import requests
import json

api_key = "mtcU6JDZ_2k8JpnnGXVWTABvAhbyk_P3Wb5VaVzg6VNuFSwxmheibDhV3agYnf8M$2a$06$xw0Yv9mLeLEfZPVtjnA9DO"

#define headers for inserting api credentials
header = {"X-Risk-Token":api_key, "accept": "application/json"}
host_url = "https://api.kennasecurity.com/vulnerability_definitions/{}"

cve_list = []
#open a input file to read cve data and opening an output file to write the response data
with open("test_insert.txt", encoding='utf-8') as cve, open("kenna.json","w", encoding='utf-8') as file:
    file.write("[")
    #read each line from the input file
    lines=cve.readlines()

    #iterate over each line to process
    for line in lines:
        #split the data where the input has comma seperated values. e.g a,b,c etc
        source_cve = line.split(",")
        #iterate over each item
        for i in source_cve:
            if i.strip() not in cve_list:
                cve_list.append(i.strip())
            else:
                continue
            try:
                #sending the request
                print(host_url.format(i))
                response = requests.get(host_url.format(i.strip()),headers=header)
            
                #print(response.json(), encoding='utf-8')
                rjson = response.json()
                result={}
                result["cve"] = i
                #formatting the output json to capture only required data
                result["description"] = rjson.get("vulnerability_definition",{}).get("description")
                result["daily_trend"] = rjson.get("vulnerability_definition",{}).get("daily_trend")
                result["predicted_exploitable"] = rjson.get("vulnerability_definition",{}).get("predicted_exploitable")
                result["predicted_exploitable_confidence"] = rjson.get("vulnerability_definition",{}).get("predicted_exploitable_confidence")
                result["successful_exploitations"] = rjson.get("vulnerability_definition",{}).get("successful_exploitations")
                result["velocity_day"] = rjson.get("vulnerability_definition",{}).get("velocity_day")
                result["velocity_month"] = rjson.get("vulnerability_definition",{}).get("velocity_month")
                result["velocity_week"] = rjson.get("vulnerability_definition",{}).get("velocity_week")
                result["cve_id"] = rjson.get("vulnerability_definition",{}).get("cve_id")
                result["cvss_score"] = rjson.get("vulnerability_definition",{}).get("cvss_score")
                result["cvss_exploit_subscore"] = rjson.get("vulnerability_definition",{}).get("cvss_exploit_subscore")
                result["cvss_impact_subscore"] = rjson.get("vulnerability_definition",{}).get("cvss_impact_subscore")
                result["cvss_vector"] = rjson.get("vulnerability_definition",{}).get("cvss_vector")
                result["cvss_temporal_score"] = rjson.get("vulnerability_definition",{}).get("cvss_temporal_score")
                result["cvss_v3_score"] = rjson.get("vulnerability_definition",{}).get("cvss_v3_score")
                result["cvss_v3_exploit_subscore"] = rjson.get("vulnerability_definition",{}).get("cvss_v3_exploit_subscore")
                result["cvss_v3_impact_subscore"] = rjson.get("vulnerability_definition",{}).get("cvss_v3_impact_subscore")
                result["cvss_v3_vector"] = rjson.get("vulnerability_definition",{}).get("cvss_v3_vector")
                result["cvss_v3_temporal_score"] = rjson.get("vulnerability_definition",{}).get("cvss_v3_temporal_score")
                result["cve_description"] =  rjson.get("vulnerability_definition",{}).get("cve_description")
                result["cvss_access_complexity"] =  rjson.get("vulnerability_definition",{}).get("cvss_access_complexity")
                result["cvss_access_vector"] =  rjson.get("vulnerability_definition",{}).get("cvss_access_vector")
                result["cvss_authentication"] =  rjson.get("vulnerability_definition",{}).get("cvss_authentication")
                result["risk_meter_score"] =  rjson.get("vulnerability_definition",{}).get("risk_meter_score")
                result["cvss_availability_impact"] =  rjson.get("vulnerability_definition",{}).get("cvss_availablity_impact")
                result["cvss_confidentiality_impact"] =  rjson.get("vulnerability_definition",{}).get("cvss_confidentiality_impact")
                result["cvss_integrity_impact"] =  rjson.get("vulnerability_definition",{}).get("cvss_integrity_impact")
                result["easily_exploitable"]  =  rjson.get("vulnerability_definition",{}).get("easily_exploitable")
                result["malware_exploitable"] =  rjson.get("vulnerability_definition",{}).get("malware_exploitable")
                result["active_internet_breach"] =  rjson.get("vulnerability_definition",{}).get("active_internet_breach")
                result["malware_count"] =  rjson.get("vulnerability_definition",{}).get("malware_count")
                result["popular_target"] =  rjson.get("vulnerability_definition",{}).get("popular_target")
                result["remote_code_execution"] =  rjson.get("vulnerability_definition",{}).get("remote_code_execution")
                result["pre_nvd_chatter"] =  rjson.get("vulnerability_definition",{}).get("pre_nvd_chatter")


                # Capture the specific list data in json response
                exploit_names = [i.get("name") for i in rjson.get("vulnerability_definition",{}).get("exploits",[]) if i.get("name") is not None ]
                result["Exploit_name"] = " , " .join(exploit_names)

                fixes = [i.get("product") for i in rjson.get("vulnerability_definition", {}).get("fixes", []) if i.get("product") is not None]
                result["Fix_Product"] = " , ".join(fixes)
                fixes1 = [i.get("url") for i in rjson.get("vulnerability_definition", {}).get("fixes", []) if i.get("url") is not None]
                result["Fix_Url"] = " , ".join(fixes1)

                vulnerable_products = [i for i in rjson.get("vulnerability_definition", {}).get("vulnerable_products", [])]
                result["Vulnerable_Products"] = " , ".join(vulnerable_products)
                file.write(json.dumps(result))
                file.write(",")
            except Exception as E:
                print(i,E)
    file.write("]")
