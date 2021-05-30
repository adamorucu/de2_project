"""
Used to fetch metadata from Github
"""
import argparse
import json
import sys
import csv
from time import sleep
from github import Github as GitHub, RateLimitExceededException

def fetch():
    GITHUB_TOKEN = "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"
    api = GitHub(GITHUB_TOKEN)
    q = "stars:50..1000000"  # The topmost currently has less than 400 000 
    result = api.search_repositories(q, sort="stars", order="desc")
    return result

def repo_to_dict(r, with_urls):
    d = {
        "stargazers_count": r.stargazers_count,
        "archive_url": r.archive_url,
        "assignees_url": r.assignees_url,
        "blobs_url": r.blobs_url,
        "branches_url": r.branches_url,
        "clone_url": r.clone_url,
        "collaborators_url": r.collaborators_url,
        "comments_url": r.comments_url,
        "commits_url": r.commits_url,
        "compare_url": r.compare_url,
        "contents_url": r.contents_url,
        "contributors_url": r.contributors_url,
        "created_at": str(r.created_at),
        "default_branch": r.default_branch,
        "description": r.description,
        "downloads_url": r.downloads_url,
        "events_url": r.events_url,
        "fork": r.fork,
        "forks": r.forks,
        "forks_count": r.forks_count,
        "forks_url": r.forks_url,
        "full_name": r.full_name,
        "git_commits_url": r.git_commits_url,
        "git_refs_url": r.git_refs_url,
        "git_tags_url": r.git_tags_url,
        "git_url": r.git_url,
        "has_downloads": r.has_downloads,
        "has_issues": r.has_issues,
        "has_wiki": r.has_wiki,
        "homepage_url": r.homepage,
        "hooks_url": r.hooks_url,
        "html_url": r.html_url,
        "id": r.id,
        "issue_comment_url": r.issue_comment_url,
        "issue_events_url": r.issue_events_url,
        "issues_url": r.issues_url,
        "keys_url": r.keys_url,
        "labels_url": r.labels_url,
        "language": r.language,
        "languages_url": r.languages_url,
        "merges_url": r.merges_url,
        "milestones_url": r.milestones_url,
        "mirror_url": r.mirror_url,
        "name": r.name,
        "notifications_url": r.notifications_url,
        "open_issues": r.open_issues,
        "open_issues_count": r.open_issues_count,
        "owner": r.owner.login,
        "pulls_url": r.pulls_url,
        "pushed_at": str(r.pushed_at),
        "size": r.size,
        "ssh_url": r.ssh_url,
        "stargazers_url": r.stargazers_url,
        "statuses_url": r.statuses_url,
        "subscribers_count": r.subscribers_count,
        "subscribers_url": r.subscribers_url,
        "subscription_url": r.subscription_url,
        "svn_url": r.svn_url,
        "tags_url": r.tags_url,
        "teams_url": r.teams_url,
        "trees_url": r.trees_url,
        "updated_at": str(r.updated_at),
        "url_url": r.url,
    }
    
    if with_urls:
        return d
        
    # Remove urls from the data if option selected
    res = {}
    for k in d.keys():
        if k[-4:] != "_url":
            res[k] = d[k]
    return res


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--with_urls", help="If present, urls will be included in the metadata", required=False, default=False, type=bool)
    parser.add_argument("--filename", help="Location of output file", default="githubrepos.csv", type=str, required=False)
    parser.add_argument("--maxcount", help="Maximum number of repos to fetch data for", type=int, required=False, default=1000)    
    return parser.parse_args()

def main():
    
    args = parse_args()
    max_count = args.maxcount
    
    result = fetch()
    
    start_from = 0
    first_item = True
    fetched_all = False
    file = open(args.filename, "w")   # create an empty file

    while not fetched_all:
        try:
            for i, r in enumerate(result):   # will always start from the first
                if i >= start_from:
                    d = repo_to_dict(r, args.with_urls)   # extract relevant fields
                
                    if first_item:             # create column headers for csv
                        c = csv.DictWriter(file, d.keys())
                        c.writeheader()
                        first_item = False
                    
                    c.writerows([d])           # write data in csv format, encoding ',', '"' etc
                    if (i + 1) % 100 == 0:
                        print("Processed", i + 1, "repos...")
                if i + 1 >= max_count:
                    break
                    
            fetched_all = True
        except RateLimitExceededException:
            start_from = i + 1
            print("Limit exceeded, waiting 60 s... ")
            sleep(60)
            print("continuing!")
            
    file.close()   
    print("Finished, output written to", args.filename)
        
if __name__ == "__main__":
    main()

