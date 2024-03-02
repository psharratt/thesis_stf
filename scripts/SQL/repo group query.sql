select * from repo where repo_id in
	(select repo_id from explorer_user_repos where login_name='psh1');