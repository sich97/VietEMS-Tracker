import sys
import requests


API_URL = "https://api.myems.vn/TrackAndTraceItemCode"

def main():
    existing_entries_file = open('existing_entries.txt', 'r')
    existing_entries = {}
    for line in existing_entries_file:
        existing_entries[line.split(": ")[0]] = line.split(": "[1])
    existing_entries_file.close()


    itemcode = ""
    if len(sys.argv) > 1:
        itemcode = sys.argv[1]

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

    new_entries = {}

    for entry in parsed_data:
        if entry["NGAY_TRANG_THAI"] not in existing_entries.keys():
            entry_parse = list(entry.values())[1:]
            entry_parse = [" ".join(element.split()) for element in entry_parse if element]

            new_entries[entry["NGAY_TRANG_THAI"]] = entry_parse[2:]

            existing_entries_file = open('existing_entries.txt', 'a')
            existing_entries_file.write(entry["NGAY_TRANG_THAI"] + ": " + str(entry_parse) + "\n")
            existing_entries_file.close()
    
    if new_entries:
        html_body = "<h1>There has been an update to your EMS tracking</h1>"

        html_body += "<table><tr><th>Date & time</th><th>Status</th><th>Location</th>"
        for datetime, data in new_entries.items():
            html_body += "<tr><td>" + datetime + "</td><td>" + str(data[0]) + "</td><td>" + str(data[1:]) + "</td></tr>"
        html_body += "</table>"

        html_body += "<br><br><a href='https://ems.com.vn/tra-cuu/tra-cuu-buu-gui?code=" + itemcode + "' target='_blank'>Link to tracking website</a>"

        print(html_body)
        return new_entries


if __name__ == "__main__":
    main()
