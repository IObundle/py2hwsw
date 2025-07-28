#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/device.h>
#include <linux/init.h> 
#include <linux/fs.h> 
#include <linux/mm.h>
#include <linux/slab.h>
#include <linux/dma-mapping.h>
#include <linux/interrupt.h>
#include <linux/types.h>
#include <asm/uaccess.h>
#include <asm/io.h>

// Disable all prints
#undef printk
#define printk(...) ((void)0)

// TODO: Do not know if this module supports concurrent access. I believe it does because no use of shared memory but have not tested it.

static struct class* class;
static struct device* device;

static void* last_physical;

static int major; 

#define DEVICE_NAME "versat"
#define CLASS_NAME  "versat_class"

static int module_release(struct inode* inodep, struct file* filp){
   printk(KERN_INFO "Device closed\n");

   return 0;
}

static int module_open(struct inode* inodep, struct file* filp){
   printk(KERN_INFO "Device opened\n");

   return 0;
}

static unsigned int numberToNextOrder(int val){
   unsigned int order = 0;
   while((1 << order) < val){
      order += 1;
   }
   return order;
}

void module_vma_close(struct vm_area_struct *vma){
   int pageSize;
   void* virtual_mem;
   int order;
   uintptr_t data = (uintptr_t) vma->vm_private_data;

   pageSize = 1 << PAGE_SHIFT;
   virtual_mem = (void*) (data & ~(pageSize - 1));
   order = (int) (data & (pageSize - 1));

   printk(KERN_NOTICE "Simple VMA close, virt %lx, Priv: %px Virt: %px Ord: %d\n ",vma->vm_start,vma->vm_private_data,virtual_mem,order);

   free_pages((unsigned long) virtual_mem,order);
}

static struct vm_operations_struct simple_remap_vm_ops = {
   .close = module_vma_close,
};

static int module_mmap(struct file* file, struct vm_area_struct* vma){
   unsigned long size;
   struct page* page;
   void* virtual_mem;
   unsigned long pageStart;
   int res;
   unsigned int order;
   int amountPages;
   int pageSize;

   size = (unsigned long)(vma->vm_end - vma->vm_start);
   pageSize = 1 << PAGE_SHIFT;
   printk(KERN_INFO "PageSize %d\n",pageSize);
   printk(KERN_INFO "Size %lu",size);

   // Only support page aligned sizes
   if((size & (pageSize - 1)) != 0){
      return -EIO;
   }

   amountPages = (size + pageSize - 1) / pageSize;
   order = numberToNextOrder(amountPages);

   printk(KERN_INFO "Size %lu %d %u\n",size,amountPages,order);
   page = alloc_pages(GFP_KERNEL,order);
   if(page == NULL){
      printk(KERN_INFO "Error allocating page\n");
      return -EIO;
   }

   // TODO: Zero out the pages.
   virtual_mem = page_address(page); //alloc_mapable_pages(pages); 
   printk(KERN_INFO "Virtual Address %px\n",virtual_mem);

   last_physical = (void*) virt_to_phys(virtual_mem);
   printk(KERN_INFO "Physical Address %px\n",last_physical);

   if(virtual_mem == NULL){
      pr_err("Failed to allocate memory\n");
      return -EIO;
   }

   pageStart = page_to_pfn(page);
   printk(KERN_INFO "PageStart %lx\n",pageStart);

   res = remap_pfn_range(vma,vma->vm_start,pageStart,size,vma->vm_page_prot);
   printk(KERN_INFO "VM Start %lx\n",vma->vm_start);
   if(res != 0){
      pr_err("Failed to remap\n");
      return -EIO;
   }

   vma->vm_private_data = (void*) ((uintptr_t)virtual_mem | (uintptr_t)order); // Store order in the lower bits that are guaranteed to be zero because virtual_mem is page aligned
   vma->vm_ops = &simple_remap_vm_ops;

   return 0;
}

long int module_ioctl(struct file *file,unsigned int cmd,unsigned long arg){
   switch(cmd){
      case 0:{
         if(copy_to_user((int*) arg,&last_physical,sizeof(void*))){
            printk(KERN_INFO "Error copying data\n");
         }
      } break;
      default:{
         printk(KERN_INFO "IOCTL not implemented %d\n",cmd);
      } break;
   }

   return 0;
}

static const struct file_operations fops = {
   .open = module_open,
   .release = module_release,
   .mmap = module_mmap,
   .unlocked_ioctl = module_ioctl,
   .owner = THIS_MODULE,
};

int versat_init(void){
   int ret = -1;

   major = register_chrdev(0, DEVICE_NAME, &fops);
   if (major < 0){
      printk(KERN_INFO "Failed to register major\n");
      ret = major;
      goto failed_major_register;
   }

   class = class_create(THIS_MODULE, CLASS_NAME);
   if (IS_ERR(class)){ 
      printk(KERN_INFO "Failed to register class\n");
      ret = PTR_ERR(class);
      goto failed_class_create;
   }

   device = device_create(class, NULL, MKDEV(major, 0), NULL, DEVICE_NAME);
   if (IS_ERR(device)) {
      printk(KERN_INFO "Failed to create device\n");
      ret = PTR_ERR(device);
      goto failed_device_create;
   }

   printk(KERN_INFO "Successfully loaded versat\n");

   return 0;

// if device successes and we add more code that can fail
   device_destroy(class, MKDEV(major, 0));  
failed_device_create:
   class_unregister(class);
   class_destroy(class); 
failed_class_create:
   unregister_chrdev(major, DEVICE_NAME);
failed_major_register:
   return ret;
}

void versat_exit(void)
{
   // This portion should reflect the error handling of this_module_init
   device_destroy(class, MKDEV(major, 0));
   class_unregister(class);
   class_destroy(class);
   unregister_chrdev(major, DEVICE_NAME);

   printk(KERN_INFO "versat unregistered!\n");
}

module_init(versat_init);
module_exit(versat_exit);
MODULE_LICENSE("GPL");