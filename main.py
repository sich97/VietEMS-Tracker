import sys
import requests

API_URL = "https://api.myems.vn/TrackAndTraceItemCode"

def main():
    language = "1"
    if len(sys.argv) > 2:
        language = sys.argv[2]

    params = {
        "itemcode": sys.argv[1],
        "language": language
    }

    # sending get request and saving the response as response object
    r = requests.get(url = API_URL, params = params)

    parsed_data = [dict(entry) for entry in list(r.json()["List_TBL_DINH_VI"])]

    for entry in parsed_data:
        print(entry)


if __name__ == "__main__":
    main()
