# SoftwareDev
Software Development Project

# Create git repo locally
Step 1: Add ssh key to github https://help.github.com/articles/generating-ssh-keys/

Step 2: Run `git clone git@github.com:TylerAldrich/SoftwareDev.git`

Step 3: ???

Step 4: Prophet

# Git usage
When making changes, start with `$ git checkout -b INITIALS_STORY_NUMBER`

ex: `$ git checkout -b TA_BACK018`

To switch between git branches A and B:

`$ git checkout A` will switch to A

`$ git checkout B` will switch to B

Any uncommited changes will get carried into the checked out branch, so if you dont want this to happen you can either commit the changes (if they are ready
to be commited), or you can stash them with `$ git stash`, and later retreive with:
`$ git stash pop`

To commit changes: 

* Add your changes to be staged for commit with 'git add X', where X = name of the file you changed. (To add all files in your current directory, you can do 'git add .')

* Type 'git status' to see which files are staged for commit and make sure its correct.

* Once all the files have been staged for commit, type `$ git commit -m HELPFUL MESSAGE HERE` (Make sure your message is actually helpful...)

Type `$ git push origin YOUR_BRANCH_NAME` to push the changes of your branch to the remote repository

To update your branch (master or a feature branch) to the newest remote code:

`$ git pull origin master` on the branch you want to update. It's best to run this frequently so that you don't work on old code.


# Merging code into Master
Once you're ready to merge your branch into the master branch (where only completed/working features live), go to the github repository, find your branch, and select 'Create Pull Request'.

Name the Pull Request (PR) something that describes what you've done. Tag someone in your group (Front end / Back end) using an '@' mention. This gives others a chance to see what's being added to the codebase, so everybody has 
a good idea about what's going on and what changes have been made.

# Style
Code should follow Google's [Python Style Rules](https://google-styleguide.googlecode.com/svn/trunk/pyguide.html#Python_Style_Rules) for uniformity.

# Testing
All code should be tested using the [Python Unit Testing Framework](https://docs.python.org/2/library/unittest.html).
