from scholarly import scholarly
from pprint import pprint

# Google Scholar
def googleScholar(author_name, uuid):
    author_id: str = str()
    authors = scholarly.search_author(author_name)
    for author in authors:
        if author['email_domain'] == uuid: # hardcored
            author_id = author['scholar_id']
            break
    if author_id is None:
        raise Exception("Author Not found")
    print("Author Found")
    
    author_profile = scholarly.search_author_id(author_id)
    author_sections = scholarly.fill(
        object=author_profile,
        sections=[
            'basics',
            'indices',
            'counts', 
            'coauthors',
            'publications',
            'public_access',
        ], # later remove sections which u don't need
    )
    # Get attributes from author profile
    url_pic = author_sections['url_picture']
    coauthors = author_sections['coauthors']
    publications = author_sections['publications']

    # pprint(scholarly.fill(publications[0]))
    # get 2 publications for now
    print("Storing Publications")
    bibs = []
    for publication in publications[:2]: # change slicing 
        complete_pub_info = scholarly.fill(
            object=publication
        )
        bibs.append(complete_pub_info['bib'])
        # pprint(complete_pub_info)
    print("Returning BIBs data")
    return bibs # please change later


if __name__ == "__main__":
    res = googleScholar("Swomya B J", "@msrit.edu")
    print(res[0].keys())
