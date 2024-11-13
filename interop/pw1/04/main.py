import requests
import json
import sys

API_ACCESS_TOKEN = ''

base_url = 'https://api.github.com'
headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': 'Bearer ' + API_ACCESS_TOKEN
}

def get_pull_requests(org, project):
    url = f'{base_url}/repos/{org}/{project}/pulls'
    response = requests.get(url, headers=headers)
    return response.json()

def get_comments(org, project, pull_number):
    url = f'{base_url}/repos/{org}/{project}/issues/{pull_number}/comments'
    response = requests.get(url, headers=headers)
    return response.json()

def get_commenters_with_count(org, project, pull_number):
    comments = get_comments(org, project, pull_number)
    commenters = {}
    for comment in comments:
        user = comment['user']['login']
        if user in commenters:
            commenters[user] += 1
        else:
            commenters[user] = 1
    return commenters

def get_issues(org, project):
    url = f'{base_url}/repos/{org}/{project}/issues'
    response = requests.get(url, headers=headers)
    return response.json()

def get_labels_with_count(org, project, issue_number):
    url = f'{base_url}/repos/{org}/{project}/issues/{issue_number}/labels'
    response = requests.get(url, headers=headers)
    labels = response.json()
    top_labels = {}
    for label in labels:
        if label['name'] in top_labels:
            top_labels[label['name']]['count'] += 1
        else:
            top_labels[label['name']] = {
                "count": 1,
                "color": label['color']
            }
    return top_labels

def main():
    if len(sys.argv) != 2:
        print('Usage: python main.py <org>/<project>')
        sys.exit(1)
    
    # Extract the organization and project from the argument
    org, project = sys.argv[1].split('/')

    # Get the pull requests
    pulls = get_pull_requests(org, project)

    # Write the pull requests to a file
    with open('04/output.json', 'w') as f:
        f.write(json.dumps(pulls))

    # Get the pull request(s) with the highest number of comments
    max_comments = 0
    pulls_with_num_comments = []
    for pull in pulls:
        comments = get_comments(org, project, pull['number'])
        pulls_with_num_comments.append((pull['title'], len(comments)))
        max_comments = max(max_comments, len(comments))
    pulls_with_max_comments = [pull for pull in pulls_with_num_comments if pull[1] == max_comments]
    print(f'The pull request(s) with the biggest number of comments is/are: {pulls_with_max_comments}')

    # Top commenters (I compute the total number of comments across all pull requests, and NOT per pull request)
    top_commenters = {}
    for pull in pulls:
        commenters = get_commenters_with_count(org, project, pull['number'])
        for commenter, count in commenters.items():
            if commenter in top_commenters:
                top_commenters[commenter] += count
            else:
                top_commenters[commenter] = count
    top_commenters = sorted(top_commenters.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f'Top 5 commenters of pull requests: {top_commenters}')

    # Top labels
    issues = get_issues(org, project)
    all_labels = {}
    for issue in issues:
        labels = get_labels_with_count(org, project, issue['number'])
        for label, value in labels.items():
            if label in all_labels:
                all_labels[label]['count'] += 1
            else:
                all_labels[label] = {
                    "count": 1,
                    "color": value['color']
                }
    top_labels = [(key, value['color'], value['count']) for key, value in all_labels.items()]
    print(f'Top 5 labels: {top_labels}')

if __name__ == '__main__':
    main()
