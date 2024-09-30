from scholarly import scholarly
from pprint import pprint
from tqdm import tqdm
from collections import defaultdict


# Google Scholar
def googleScholar(author_name, uuid):
    author_id: str = str()
    authors = scholarly.search_author(author_name)
    for author in authors:
        if author['email_domain'] == uuid: # hardcored
            author_id = author['scholar_id']
            break
    if not author_id:
        return None
    print("Author Found", author_id)
    
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
    url_pic = author_sections.get('url_picture', None)
    coauthors = author_sections.get('coauthors', None)
    publications = author_sections.get('publications', None)

    # pprint(scholarly.fill(publications[0]))
    # get 2 publications for now
    print("Storing Publications")
    bibs = []
    for publication in tqdm(publications[:]): # change slicing 
        complete_pub_info = scholarly.fill(
            object=publication
        )
        bibs.append(complete_pub_info['bib'])
        # pprint(complete_pub_info)
    print("Returning BIBs data")
    return bibs # please change later


# New Code
class GoogleScholar:
    def __call__(self, scholar_name, org_domain, start_year, end_year):
        scholar_profile = self.getScholarProfile(scholar_name, org_domain)
        if scholar_profile is None: return None
        scholar_publications = self.getScholarPublications(scholar_profile, start_year, end_year)
        return scholar_publications

    def getScholarProfile(self, author_name, org_domain):
        authors = scholarly.search_author(author_name)
        for author in authors:
            if author['email_domain'] == org_domain:
                author_profile = scholarly.fill(author)
                return author_profile
        return None

    def getScholarPublications(self, author_profile, start_year, end_year):
        df = defaultdict(list) 
        # Get publications based on start and end year
        publications = author_profile['publications']
        for publication in tqdm(publications): 
            pub_year = publication['bib'].get("pub_year", None)
            if not pub_year:
                continue
            if start_year <= int(pub_year) <= end_year:
                # Fill basics author details
                df["author_name"].append(author_profile.get("name", None))
                df["interests"].append(author_profile.get("interests", None))
                # Fill publication info
                bibtex = scholarly.fill(
                    object=publication
                )["bib"]
                df["paper_title"].append(bibtex.get("title", None))
                df["abstract"].append(bibtex.get("abstract", None))
                df["pub_year"].append(bibtex.get("pub_year", None))
                df["authors"].append(bibtex.get("author", None))
                df["Journal"].append(bibtex.get("journal", None))
        return df


if __name__ == "__main__":
    res = googleScholar("Swomya B J", "@msrit.edu")
    print(res[0].keys())

