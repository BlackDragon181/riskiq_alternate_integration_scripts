import requests
import json
import time

host_url = "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId{}"

with open("test_insert.txt") as cve, open("nvd.json", "w") as file:
    file.write("[")
    lines = cve.readlines()

    for line in lines:
        source_cve = line.split(",")

        for i in source_cve:
            time.sleep(2)
            print(host_url.format(i.strip()))
            response = requests.get(host_url.format(i.strip()))
            print(response.text)
            rjson = response.json()
            result = {}
            result["cve"] = i

            #cvss V3 score
            result["CVSS BaseScore"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV3", {}).get("cvssV3", {}).get("baseScore")
            result["Severity"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV3", {}).get("cvssV3", {}).get("baseSeverity")
            result["VectorString"] = rjson.get("result",{}).get("CVE_Items",{})[0].get("impact",{}).get("baseMetricV3",{}).get("cvssV3",{}).get("vectorString")
            result["AttackVector"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV3", {}).get("cvssV3", {}).get("attackVector")
            result["AttackComplexity"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV3", {}).get("cvssV3", {}).get("attackComplexity")
            result["PrivilegesRequired"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV3", {}).get("cvssV3", {}).get("privilegesRequired")
            result["UserInteraction"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV3", {}).get("cvssV3", {}).get("userInteraction")
            result["Scope"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV3", {}).get("cvssV3", {}).get("scope")
            result["ConfidentialityImpact"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV3", {}).get("cvssV3", {}).get("confidentialityImpact")
            result["IntegrityImpact"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV3", {}).get("cvssV3", {}).get("integrityImpact")
            result["AvailabilityImpact"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV3", {}).get("cvssV3", {}).get("availabilityImpact")
            result["ExploitabilityScore"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get( "baseMetricV3", {}).get("exploitabilityScore")
            result["ImpactScore"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV3", {}).get("impactScore")

            #cvss  V2 Score
            result["CVSS v2 BaseScore"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV2", {}).get("cvssV2", {}).get("baseScore")
            result["CVSS V2 VectorString"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV2", {}).get("cvssV2", {}).get("vectorString")
            result["CVSS V2 AccessVector"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV2", {}).get("cvssV2", {}).get("accessVector")
            result["CVSS V2 AccessComplexity"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV2", {}).get("cvssV2", {}).get("accessComplexity")
            result["CVSS V2 ConfidentialityImpact"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV2", {}).get("cvssV2", {}).get("confidentialityImpact")
            result["CVSS V2 IntegrityImpact"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV2", {}).get("cvssV2", {}).get("integrityImpact")
            result["CVSS V2 AvailabilityImpact"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV2", {}).get("cvssV2", {}).get("availabilityImpact")
            result["CVSS V2 Severity"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV2", {}).get("severity")
            result["CVSS V2 ExploitabilityScore"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV2", {}).get("exploitabilityScore")
            result["CVSS V2 ImpactScore"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV2", {}).get("impactScore")
            result["CVSS V2 ObtainUserPrivilege"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV2", {}).get("obtainUserPrivilege")
            result["CVSS V2 ObatainOtherPrivilege"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get( "baseMetricV2", {}).get("obtainOtherPrivilege")
            result["CVSS V2 UserInteractionRequired"] = rjson.get("result", {}).get("CVE_Items", {})[0].get("impact", {}).get("baseMetricV2", {}).get("userInteractionRequired")

            file.write(json.dumps(result))
            file.write(",")

    file.write("]")
