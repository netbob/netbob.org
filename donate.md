---
layout: page
title: Support My Work
permalink: /donate/
---

If you enjoy my software experiments, embedded programming guides, or science fiction manuscripts, feel free to drop a tip. 

To ensure absolute financial privacy, every transaction utilizes a dynamically rotating destination address via an automated xPub framework. Your personal information is never collected or logged.

<!-- Fixed Target: Clean, styled wrapper with a physical button element inside -->
<div id="blockonomics-widget" style="text-align: center; margin-top: 30px; margin-bottom: 30px;">
  <button id="pay-btn" style="background-color: #2b82c9; color: white; padding: 12px 30px; font-size: 1.1rem; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    Click to Enter Donation Amount
  </button>
</div>

<!-- Fixed Script Path: Points directly to the Blockonomics core app framework -->
<script type="text/javascript" src="https://blockonomics.co"></script>
<script type="text/javascript">
  document.addEventListener("DOMContentLoaded", function() {
    var payBtn = document.getElementById("pay-btn");
    if (payBtn) {
      payBtn.addEventListener("click", function(e) {
        e.preventDefault();
        if (typeof blockonomics_payment_widget === "function") {
          blockonomics_payment_widget({
            uid: "1ab848ead2374f16",
            msg_area: "blockonomics-widget"
          });
        }
      });
    }
  });
</script>
