`timescale 1ns / 1ps

`define R 0
`define W 1
`define F 2


`define IOB_GET_NBYTES(WIDTH) (WIDTH/8 + |(WIDTH%8))
`define IOB_WORD_ADDRESS(ADDR) ((ADDR>>2)<<2)

`define IOB_BYTE_OFFSET(ADDR) (ADDR%(32/8))

`define IOB_GET_WDATA(ADDR, DATA) (DATA<<(8*`IOB_BYTE_OFFSET(ADDR)))
`define IOB_GET_WSTRB(ADDR, WIDTH) (((1<<`IOB_GET_NBYTES(WIDTH))-1)<<`IOB_BYTE_OFFSET(ADDR))
`define IOB_GET_RDATA(ADDR, DATA, WIDTH) ((DATA>>(8*`IOB_BYTE_OFFSET(ADDR)))&((1<<WIDTH)-1))



module iob_v_tb;

   // Signals (examples - adjust as needed for your design)
   reg clk;
   reg rst;
   
   // File handles
   integer c2v_read_fp = 0;
   integer v2c_write_fp = 0;
   
   // Variables
   integer req=-100, ack=0, mode=-100, address=-100, data=-100;

   // Example test sequence (replace with your actual test logic)
   initial begin
      clk = 0;
      rst = 1;
      #10;
      rst = 0;
      #10;
      
      // Server loop
      while(n < 10000) begin
         //read request
         c2v_read_fp = $fopen("c2v.txt", "rb");
         if (c2v_read_fp != 0) begin
            if ($fscanf(c2v_read_fp, "%08x %08x %08x %08x\n", req, mode, address, data)) begin 
               $display("V: req=%08x mode=%08x address=%08x data=%08x", req, mode, address, data);

               //check if request number matches with ack number
               if(req == ack) begin
                  v2c_write_fp = $fopen("v2c.txt", "wb");
                  if (v2c_write_fp != 0) begin
                     //process request
                     if(mode == `F) begin //finish request
                        $display("V: finish request");
                        $finish;
                     end
                     if(mode == `R) begin //read request
                        iob_read(address, data, 32);
                        //send ack  and data
                        $fdisplay(v2c_write_fp, "%08x %08x %08x %08x\n", ack, mode, address, data);
                        $display("V: read request: adress=%08x data=%08x", address, data);
                     end
                     else if(mode == `W) begin //write request
                        iob_write(address, data, 32);
                        //send ack
                        $fdisplay(v2c_write_fp, "%08x %08x %08x %08x\n", ack, mode, address, data);
                        $display("V: write request: adress=%08x data=%08x", address, data);
                     end
                     $fclose(v2c_write_fp);
                  end // if (v2c_write_fp != 0)
                  ack = ack + 1;
               end // if (req == ack)
            end // if (fscanf_ret == 4)
            $fclose(c2v_read_fp);
         end // if (c2v_read_fp != 0)
         @(posedge clk);//advance clock
         n = n + 1;
      end // while (1)
   end // initial begin



   // Instantiate the Unit Under Test (UUT)
   iob_uut uut 
     (
      .clk_i          (clk),
      .arst_i         (arst),
      .cke_i          (cke),

      .iob_valid_i (iob_valid_i),
      .iob_addr_i  (iob_addr_i),
      .iob_wdata_i (iob_wdata_i),
      .iob_wstrb_i (iob_wstrb_i),
      .iob_rvalid_o(iob_rvalid_o),
      .iob_rdata_o  (iob_rdata_o),
      .iob_ready_o  (iob_ready_o)
      );

   // Write data to IOb Native slave
   task iob_write;
      input [`IOB_UART_CSRS_ADDR_W-1:0] addr;
      input [31:0]                      data;
      input [$clog2(32):0]              width;
      
      begin
         @(posedge clk) #1 iob_valid_i = 1;  //sync and assign
         iob_addr_i  = `IOB_WORD_ADDRESS(addr);
         iob_wdata_i = `IOB_GET_WDATA(addr, data);
         iob_wstrb_i = `IOB_GET_WSTRB(addr, width);
         
         #1 while (!iob_ready_o) #1;
         
         @(posedge clk) iob_valid_i = 0;
         iob_wstrb_i = 0;
      end
   endtask

   // Read data from IOb Native slave
   task iob_read;
      input [`IOB_UART_CSRS_ADDR_W-1:0] addr;
      output [31:0]                     data;
      input [$clog2(32):0]              width;
      
      begin
         @(posedge clk) #1 iob_valid_i = 1;
         iob_addr_i = `IOB_WORD_ADDRESS(addr);
         iob_wstrb_i = 0;
         
         #1 while (!iob_ready_o) #1;
         @(posedge clk) #1 iob_valid_i = 0;
         
         while (!iob_rvalid_o) #1;
         data = #1 `IOB_GET_RDATA(addr, iob_rdata_o, width);
      end
   endtask
   
   
   
   always #5 clk = ~clk; // Clock generation

   
endmodule
