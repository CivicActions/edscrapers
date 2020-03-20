import tools.dataset_metrics.metrics as metrics


if __name__ == "__main__":
    #print(metrics.list_domain())
    #print('')
    #print(metrics.list_domain('air'))
    #print('')
    #print(metrics.list_exclusive_domain())
    #print('')
    #print(metrics.list_exclusive_domain('air', 'datopian'))
    #print('')
    #print(metrics.list_highest_resources_from_pages())
    #print('')
    #print(metrics.list_highest_resources_from_pages(scraper='air'))
    #print('')
    #print(metrics.data_json_compare())
    #print('')
    #print(metrics.list_intersection_domain())

    metrics.list_domain()
    metrics.list_domain(scraper='air')
    metrics.list_exclusive_domain()
    metrics.list_exclusive_domain(scraper='air', compare_scraper='datopian')
    metrics.list_intersection_domain()
    metrics.list_highest_resources_from_pages()
    metrics.list_highest_resources_from_pages(scraper='air')
    metrics.data_json_compare()
