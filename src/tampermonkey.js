// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://messages.google.com/web/conversations/3
// @icon         https://www.google.com/s2/favicons?domain=google.com
// @grant        none
// ==/UserScript==
// Change the @match value above.

(function () {
    'use strict';

    function getOtp(message) {
        let match = message.match(/\d{6}/);
        return match[0];
    }

    const lastMessageSelector =
        'mw-conversation-container mws-messages-list mws-bottom-anchored mws-message-wrapper:last-of-type';

    function checkNewOtp() {
        const elem = document.querySelector(lastMessageSelector);

        if (!elem) {
            return;
        }

        debugger;

        const otp = getOtp(elem.innerText);
        const existingOtp = window.localStorage.getItem('otp', null);

        if (existingOtp === otp) {
            return;
        }

        window.localStorage.setItem('otp', otp);

        // Change the port. Should match config's "port" value.
        fetch(`http://localhost:8888/otp?otp=${otp}`, {
            method: 'POST',
        }).catch(() => {
        });
    }

    const interval = setInterval(checkNewOtp, 5000);
})();
