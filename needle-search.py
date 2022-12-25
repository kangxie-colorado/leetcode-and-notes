import asyncio
import time
import requests
import concurrent.futures


MOZILLAURL = "https://hiring.cloudops.mozgcp.net/api/orgs/mozilla/repos"
MOZILLASVCURL = "https://hiring.cloudops.mozgcp.net/api/orgs/mozilla-services/repos"

# version 1: simply callikng pagenaed api to get all repos per page


def solution_simple(needles):
    def getRepos(url):
        # simply return all repos
        # it will be obtained by the pagenated api calls
        allDone = False
        repos = None
        page = 1
        while not allDone:
            pageDone = False
            retry = 3
            while not pageDone and retry > 0:
                try:
                    repos = requests.get(f"{url}?",  params={
                                         'page': page}).json()
                    pageDone = True
                except requests.exceptions.Timeout:
                    retry -= 1
                    continue
                except requests.exceptions.InvalidJSONError:
                    print(f"Invalid data obtained from {url}?page={page}")
                except requests.exceptions.RequestException as e:
                    # more exceptions can be hanlded if needed
                    print(f"Cannot obtain data from {url}?page={page}")
                    raise SystemExit(e)

            if not repos:
                allDone = True
            yield repos
            page += 1

    res = [0 for _ in needles]

    def process(url):
        for repos in getRepos(url):
            for repo in repos:
                for i, needle in enumerate(needles):
                    if needle in repo["name"]:
                        res[i] += 1

    process(MOZILLAURL)
    process(MOZILLASVCURL)

    return res


def solution_mt(needles):
    """
    I did some research and found out that 
    1. mozilla has 75 pages
    2. mozilla-services has 13 pages
    so I think I could use multi-thread to make the code finish sooner 

    okay.. I got warning - Network usage beyond threshold!
    """

    res = [0 for _ in needles]

    def getRepos(url, page):
        done = False
        retry = 3
        while not done and retry > 0:
            try:
                repos = requests.get(f"{url}?",  params={'page': page}).json()
                done = True
            except requests.exceptions.Timeout:
                retry -= 1
                continue
            except requests.exceptions.InvalidJSONError:
                print(f"Invalid data obtained from {url}?page={page}")
            except requests.exceptions.RequestException as e:
                # more exceptions can be hanlded if needed
                print(f"Cannot obtain data from {url}?page={page}")
                raise SystemExit(e)

        return repos

    def process(url):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for page in range(1, 100):
                futures.append(executor.submit(getRepos, url, page))

            for repos in concurrent.futures.as_completed(futures):
                for repo in repos.result():
                    for i, needle in enumerate(needles):
                        if needle in repo["name"]:
                            res[i] += 1

    process(MOZILLAURL)
    process(MOZILLASVCURL)
    return res


def solution_async(needles):
    res = [0 for _ in needles]

    async def getRepos(url, page):
        done = False
        retry = 3
        while not done and retry > 0:
            try:
                repos = requests.get(f"{url}?",  params={'page': page}).json()
                done = True
            except requests.exceptions.Timeout:
                retry -= 1
                continue
            except requests.exceptions.InvalidJSONError:
                print(f"Invalid data obtained from {url}?page={page}")
            except requests.exceptions.RequestException as e:
                # more exceptions can be hanlded if needed
                print(f"Cannot obtain data from {url}?page={page}")
                raise SystemExit(e)

        return repos
    
    async def process(url, maxpage):
        results = await asyncio.gather(*(getRepos(url, page) for page in range(1, maxpage+1)))

        for repos in results:
            for repo in repos:
                for i, needle in enumerate(needles):
                    if needle in repo["name"]:
                        res[i] += 1

    async def main():
        runMozilla = process(MOZILLAURL, 75)
        runMozillaSvc = process(MOZILLASVCURL, 13)

        await asyncio.gather(*[runMozilla, runMozillaSvc])

    asyncio.run(main())

    return res

def solution(needles):
    return solution_async(needles)


print(solution(["moz","firefox","persona"]))