import os
import requests

from .searchcodeapicaller import SearchcodeApiCaller


def work(outputdir, base_url, *, start=0, offset=1, per_page=20, num_limit=0):
    """
    Call searchcode api starting from page={start} and with {offset} pages.
    Stop when result is empty.
    Only doenload files from github.
    Download files from master branch, then try develop branch if master branch doesn't exist.

    Downloaded files will be named as {username}_{reponame}_{path_to_file}_{filename}.py
    Files with the same name will be wiped out.

    Arguments:
        outputdir:
            A directory to put all the output file
        base_url:
            Searchcode api url.

    Keyword Arguments:
        start:
            Starting page. Start from 0.
        offset:
            Offset pages. p=start, p=start + offset ...
        per_page:
            Number of repository per page (per request).
        num_limit:
            Numer of repository to download accross all threads. Set 0 for no limit.
    """
    BRANCH = ['master', 'develop', 'dev', 'staging']

    github_raw = 'https://raw.githubusercontent.com/'

    caller = SearchcodeApiCaller()
    page = start - offset

    while True:
        page += offset

        # return when reach download limit
        if num_limit > 0 and page * per_page > num_limit:
            return

        url = f'{base_url}&per_page={per_page}&p={page}'
        res = caller.call(url)

        if res is None or res['results'] is None or not res['results']:
            return

        # max number
        result_repos = res['results']
        if num_limit > 0:
            result_repos = result_repos[:max(
                min(len(res), num_limit - page * per_page), 0)]

        for result in result_repos:
            ## form url to get target file.
            # parse username
            username = result['repo'].find('github.com/')
            username = result['repo'][username + 11:]
            username = username[:username.find('/')]

            # try branches in BRANCH in order
            success = False
            for branch in BRANCH:
                # form url
                file_url = f'{github_raw}{username}/{result["name"]}/{branch}'
                if result['location']:
                    file_url = f'{file_url}{result["location"]}'
                file_url = f'{file_url}/{result["filename"]}'

                # download file and store it
                file_res = requests.get(file_url)
                if file_res.ok:
                    # filename
                    ofn = os.path.join(
                        outputdir,
                        f'{username}_{result["name"]}_{result["location"].replace(os.path.sep, "_")}_{result["filename"]}'
                    )
                    try:
                        with open(ofn, 'bw') as of:
                            of.write(file_res.content)
                    except Exception as e:
                        print(e)
                    success = True
                    break

            if not success:
                print(
                    f'File not found: repo={result["repo"]}, loc={result["location"]}, file={result["filename"]}'
                )
