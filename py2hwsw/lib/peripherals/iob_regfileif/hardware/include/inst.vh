// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

   //
   // /*<InstanceName>*/
   //

   iob_regfileif /*<InstanceName>*/
     (
      .clk     (clk),
      .rst     (reset),

      // Register file interface
      .valid_ext   (/*<InstanceName>*/_valid),
      .address_ext (/*<InstanceName>*/_address),
      .wdata_ext   (/*<InstanceName>*/_wdata),
      .wstrb_ext   (/*<InstanceName>*/_wstrb),
      .rdata_ext   (/*<InstanceName>*/_rdata),
      .ready_ext   (/*<InstanceName>*/_ready),

      // CPU interface
      .valid       (subordinates_req[`valid(`/*<InstanceName>*/)]),
      .address     (subordinates_req[`address(`/*<InstanceName>*/,`iob_regfileif_csrs_ADDR_W+2)-2]),
      .wdata       (subordinates_req[`wdata(`/*<InstanceName>*/)]),
      .wstrb       (subordinates_req[`wstrb(`/*<InstanceName>*/)]),
      .rdata       (subordinates_resp[`rdata(`/*<InstanceName>*/)]),
      .ready       (subordinates_resp[`ready(`/*<InstanceName>*/)])
      );
