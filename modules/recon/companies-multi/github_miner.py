from recon.core.module import BaseModule
from urllib import quote_plus

class Module(BaseModule):
    meta = {
        'name': 'Github Resource Miner',
        'author': 'Tim Tomes (@LaNMaSteR53)',
        'description': 'Uses the Github API to enumerate repositories and member profiles associated with a company search string. Updates the respective tables with the results.',
        'query': 'SELECT DISTINCT company FROM companies WHERE company IS NOT NULL',
    }

    def module_run(self, companies):
        for company in companies:
            self.heading(company, level=0)
            # enumerate members
            self.heading('Members', level=1)
            members = self.query_github_api('/orgs/%s/members' % (quote_plus(company)))
            for member in members:
                data = {
                    'username': member['login'],
                    'url': member['html_url'],
                    'notes': company,
                    'resource': 'Github',
                    'category': 'coding',
                }
                self.output('%s (%s)' % (data['username'], data['url']))
                self.add_profiles(**data)
            # enumerate repositories
            self.heading('Repositories', level=1)
            repos = self.query_github_api('/orgs/%s/repos' % (quote_plus(company)))
            for repo in repos:
                data = {
                    'name': repo['name'],
                    'owner': repo['owner']['login'],
                    'description': repo['description'],
                    'url': repo['html_url'],
                    'resource': 'Github',
                    'category': 'repo',
                }
                self.output('%s - %s' % (data['name'], data['description']))
                self.add_repositories(**data)