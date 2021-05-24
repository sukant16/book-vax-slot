import copy
from types import SimpleNamespace
from time import sleep

import fire as fire
import requests

from utils import (
    check_and_book,
    BENEFICIARIES_URL,
    display_info_dict,
    get_saved_user_info,
    reauthorize,
)


def main(filename):
    try:
        base_request_header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/39.0.2171.95 Safari/537.36",
            # "x-api-key": "3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi"
        }

        collected_details = get_saved_user_info(filename)
        display_info_dict(collected_details)

        while True:
            info = SimpleNamespace(**get_saved_user_info(filename))
            request_header = copy.deepcopy(base_request_header)
            request_header["Authorization"] = info.auth

            # call function to check and book slots
            status = check_and_book(
                request_header,
                info.beneficiary_dtls,
                info.location_dtls,
                preferred_slot=info.preferred_slot,
                min_slots=info.minimum_slots,
            )

            if isinstance(status, bool) and status == False:
                print("Reauthorizing...")
                reauthorize(filename=filename) 
            # check if token is still valid
            else:
                continue
                # beneficiaries_list = requests.get(BENEFICIARIES_URL, headers=request_header)
                # print("status_code:", beneficiaries_list.status_code)
                # print("beneficiaries", beneficiaries_list)
                # if beneficiaries_list.status_code != 200:
                #     # if token invalid, regenerate OTP and new token
                #     print("Reauthorizing...")
                #     reauthorize(filename=filename)

    except Exception as e:
        print(str(e))
        print("Exiting Script")


if __name__ == "__main__":
    fire.Fire(main)
