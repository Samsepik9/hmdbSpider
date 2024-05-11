import requests
from bs4 import BeautifulSoup

def get_metabolite_info(hmdb_id, proxies=None):
    url = f"https://hmdb.ca/metabolites/{hmdb_id}"
    response = requests.get(url, proxies=proxies, timeout=15)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 更新选择器以匹配当前网站的HTML结构
        name = soup.find("h1", {"class": "page-header"}).text.strip() if soup.find("h1", {"class": "page-header"}) else "Name not found"
        chemical_formula = soup.find("dt", text="Chemical Formula").find_next_sibling("dd").text.strip() if soup.find("dt", text="Chemical Formula") else "Chemical Formula not found"
        description = soup.find("dt", text="Description").find_next_sibling("dd").text.strip() if soup.find("dt", text="Description") else "Description not found"
        
        return {
            "name": name,
            "chemical_formula": chemical_formula,
            "description": description
        }
    else:
        print(f"Failed to retrieve information for metabolite {hmdb_id}")
        return None

if __name__ == "__main__":
    metabolite_id = "HMDB0061810"
    # 如果不需要代理，将proxies设置为None
    # proxies = {
    #     'http': 'http://127.0.0.1:10809',
    #     # 'https': 'http://10.10.1.10:1080',
    # }
    proxies = None
    
    info = get_metabolite_info(metabolite_id, proxies)
    
    if info:
        print(f"Metabolite: {info['name']}")
        print(f"Chemical Formula: {info['chemical_formula']}")
        print(f"Description: {info['description']}")
