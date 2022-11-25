import requests
import json
import time

host_url = "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={}"

with open("test_insert.txt") as cve, open("nvd.json", "w") as file:
    file.write("[")
    lines = cve.readlines()

    for line in lines:
        source_cve = line.split(",")

        for i in source_cve:
            time.sleep(5)
            try:
                print(host_url.format(i.strip()))
                response = requests.get(host_url.format(i.strip()))
                print(response.text)
                rjson = response.json()
                result = {}
                result["cve"] = i

                result["Id"] = rjson.get("vulnerabilities")[0].get("cve",{}).get("Id",'')
                result["descriptions"] = "".join([i.get('value') for i in rjson.get("vulnerabilities")[0].get("cve",{}).get('descriptions',[]) if i.get('lang') == 'en'])
                result["source"] = rjson.get("vulnerabilities")[0].get("cve",{}).get("metrics",{}).get("cvssMetricV31",[])[0].get("source",'')
                result["vectorString"] = rjson.get("vulnerabilities")[0].get("cve",{}).get("metrics",{}).get("cvssMetricV31",[])[0].get("cvssData",{}).get("vectorString")
                result["attackComplexity"] = rjson.get("vulnerabilities")[0].get("cve",{}).get("metrics",{}).get("cvssMetricV31",[])[0].get("cvssData",{}).get("attackcomplexity")
                result["attackVector"] = rjson.get("vulnerabilities")[0].get("cve",{}).get("metrics",{}).get("cvssMetricV31",[])[0].get("cvssData",{}).get("attackVector")
                result["privilegesRequired"] = rjson.get("vulnerabilities")[0].get("cve",{}).get("metrics",{}).get("cvssMetricV31",[])[0].get("cvssData",{}).get("privilegesRequired")
                result["userInteraction"] = rjson.get("vulnerabilities")[0].get("cve",{}).get("metrics",{}).get("cvssMetricV31",[])[0].get("cvssData",{}).get("userInteraction")
                result["confidentialityImpact"] = rjson.get("vulnerabilities")[0].get("cve",{}).get("metrics",{}).get("cvssMetricV31",[])[0].get("cvssData",{}).get("confidentialityImpact")
                result["integrityImpact"] = rjson.get("vulnerabilities")[0].get("cve",{}).get("metrics",{}).get("cvssMetricV31",[])[0].get("cvssData",{}).get("integrityImpact")
                result["availabilityImpact"] = rjson.get("vulnerabilities")[0].get("cve",{}).get("metrics",{}).get("cvssMetricV31",[])[0].get("cvssData",{}).get("availabilityImpact")
                result["baseScore"] = rjson.get("vulnerabilities")[0].get("cve",{}).get("metrics",{}).get("cvssMetricV31",[])[0].get("cvssData",{}).get("baseScore")
                result["baseSeverity"] = rjson.get("vulnerabilities")[0].get("cve",{}).get("metrics",{}).get("cvssMetricV31",[])[0].get("cvssData",{}).get("baseSeverity")
                result["exploitabilityScore"] = rjson.get("vulnerabilities")[0].get("cve",{}).get("metrics",{}).get("cvssMetricV31",[])[0].get("exploitabilityScore")
                result["impactScore"] = rjson.get("vulnerabilities")[0].get("cve",{}).get("metrics",{}).get("cvssMetricV31",[])[0].get("impactScore")
                
            except Exception as E:
                print(E)
            file.write(json.dumps(result))
            file.write(",")

    file.write("]")
