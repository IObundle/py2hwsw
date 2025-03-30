// SPDX-FileCopyrightText: 2025 IObundle
//
// SPDX-License-Identifier: MIT

   //
   // GPIO
   //

   iob_gpio gpio0
     (
      .clk     (clk),
      .rst     (rst),

      // Registers interface
      .gpio_input (gpio_input),
      .gpio_output (gpio_output),
      .gpio_output_enable (gpio_output_enable),

      // CPU interface
      .valid   (subordinates_req[`valid(`GPIO)]),
      .address (subordinates_req[`address(`GPIO,`iob_gpio_csrs_ADDR_W+2)-2]),
      .wdata   (subordinates_req[`wdata(`GPIO)]),
      .wstrb   (subordinates_req[`wstrb(`GPIO)]),
      .rdata   (subordinates_resp[`rdata(`GPIO)]),
      .ready   (subordinates_resp[`ready(`GPIO)])
      );
