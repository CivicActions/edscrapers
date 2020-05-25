import os
import requests

class CkanApi():

    def __init__(self):

        ckan_host = os.getenv('CKAN_HOST', 'https://us-ed-testing.ckan.io')
        self.api_endpoint_url = '{}/api/action/ed_scraping_dashboard'.format(ckan_host)
        self.data = {}
        response = requests.get(self.api_endpoint_url).json()

        if response.get("result", False):
            self.data = response.get("result", {})

    def total_datasets(self):
        count_dict = self.data.get("count", {})
        return count_dict.get("package", 0)

    def total_scraped_datasets(self):
        count_dict = self.data.get("count", {})
        return count_dict.get("package_scraped", 0)

    def total_amended_datasets(self):
        count_dict = self.data.get("count", {})
        return count_dict.get("package_amended", 0)

    def total_manual_datasets(self):
        count_dict = self.data.get("count", {})
        return count_dict.get("package_manual", 0)

    def total_scraped_resources(self):
        count_dict = self.data.get("count", {})
        return count_dict.get("resource_scraped", 0)

    def total_scraped_pages(self):
        count_dict = self.data.get("count", {})
        return count_dict.get("page", 0)

    def total_scraped_domains(self):
        count_dict = self.data.get("count", {})
        return count_dict.get("domain", 0)

    def datasets_by_publisher(self):
        lst = []
        organization_dict = self.data.get("organization", {})
        for key, value in organization_dict.items():
            name = key
            count = value.get("package_count", 0)
            lst.append( (name, count) )
        return lst

    def resources_by_publisher(self):
        lst = []
        organization_dict = self.data.get("organization", {})
        for key, value in organization_dict.items():
            name = key
            count = value.get("resource_count", 0)
            lst.append( (name, count) )
        return lst

    def datasets_by_domain(self):
        lst = []
        organization_dict = self.data.get("domain", {})
        for key, value in organization_dict.items():
            name = key
            count = value.get("package_count", 0)
            lst.append( (name, count) )
        return lst

    def resources_by_domain(self):

        lst = []
        organization_dict = self.data.get("domain", {})
        for key, value in organization_dict.items():
            name = key
            count = value.get("resource_count", 0)
            lst.append( (name, count) )
        return lst






