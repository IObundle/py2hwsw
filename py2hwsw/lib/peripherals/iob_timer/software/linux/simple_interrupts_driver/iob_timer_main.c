/*
 * SPDX-FileCopyrightText: 2025 IObundle
 *
 * SPDX-License-Identifier: MIT
 */

/*
 * This driver binds to the iob_timer device, retrieves its IRQ from the Device
 * Tree, and registers a simple interrupt handler that logs when the timer
 * fires. It serves as a minimal example of platform device registration and IRQ
 * handling in the Linux kernel.
 */

#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/interrupt.h>
#include <linux/of.h>

/*
 * IRQ handler for the iob_timer device.
 * This function is called by the kernel when the device's interrupt fires.
 */
static irqreturn_t iob_timer_irq_handler(int irq, void *dev_id) {
  pr_info("iob_timer: interrupt fired (irq=%d)\n", irq);
  return IRQ_HANDLED;
}

/*
 * Probe function called when a matching platform device is found.
 * It retrieves the device IRQ from firmware/DT and registers an interrupt
 * handler for it.
 */
static int iob_timer_probe(struct platform_device *pdev) {
  int irq, ret;

  /* Get the first IRQ resource assigned to this platform device. */
  irq = platform_get_irq(pdev, 0);
  if (irq < 0)
    return dev_err_probe(&pdev->dev, irq, "failed to get irq\n");

  /*
   * Request ownership of the IRQ line and associate it with our handler.
   * devm_request_irq() makes the allocation device-managed, so it will be
   * released automatically when the device is removed.
   */
  ret = devm_request_irq(&pdev->dev, irq, iob_timer_irq_handler, 0,
                         dev_name(&pdev->dev), &pdev->dev);
  if (ret)
    return dev_err_probe(&pdev->dev, ret, "failed to request irq %d\n", irq);

  /* Informational message showing that the driver successfully bound. */
  dev_info(&pdev->dev, "bound, irq=%d\n", irq);
  return 0;
}

/*
 * Remove function called when the device is unbound.
 * No explicit cleanup is needed because the IRQ was requested with devm_*().
 */
static int iob_timer_remove(struct platform_device *pdev) { return 0; }

/*
 * Device Tree match table.
 * This tells the kernel which DT compatible string should bind to this driver.
 */
static const struct of_device_id iob_timer_of_match[] = {
    {.compatible = "iobundle,iob_timer"}, {}};
MODULE_DEVICE_TABLE(of, iob_timer_of_match);

/*
 * Platform driver structure describing this driver to the kernel.
 * It connects the probe/remove callbacks and the OF match table.
 */
static struct platform_driver iob_timer_driver = {
    .probe = iob_timer_probe,
    .remove = iob_timer_remove,
    .driver =
        {
            .name = "iob_timer_irq_demo",
            .of_match_table = iob_timer_of_match,
        },
};

/* Register the platform driver at module load time. */
module_platform_driver(iob_timer_driver);

MODULE_LICENSE("Dual MIT/GPL");
MODULE_AUTHOR("IObundle");
MODULE_DESCRIPTION("Minimal iob_timer IRQ demo");
