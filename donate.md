---
layout: page
title: Support My Work
permalink: /donate/
---

If you enjoy my software experiments, embedded programming guides, or science fiction manuscripts, feel free to drop a tip. 

To ensure absolute financial privacy, every transaction utilizes a dynamically rotating destination address via an automated xPub framework. Your personal information is never collected or logged.

<!-- The Fixed Standalone Native Target Element -->
<div id="blockonomics-widget" style="text-align: center; margin-top: 30px; margin-bottom: 30px;"></div>

<!-- The Blockonomics Operational Script Engine -->
<script type="text/javascript" src="https://www.blockonomics.co/js/pay_widget.js"></script>
<script type="text/javascript">
  document.addEventListener("DOMContentLoaded", function() {
    if (typeof blockonomics_payment_widget === "function") {
      blockonomics_payment_widget({
        uid: "1ab848ead2374f16",
        msg_area: "blockonomics-widget"
      });
    }
  });
</script>
