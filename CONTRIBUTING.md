# Participiant: How to Contribute

1. **Visit the HackNight 6.0 Leaderboard**:
   Browse the leaderboard and choose a repository you'd like to contribute to!

2. **Check for Open Issues**:
   Look for any open issues in the repository. If you find one that interests you, ask to be assigned to it by commenting on the issue.

3. **Setup Your Codebase**:
   - **Fork** the repository to your GitHub account and copy it's clone URL
   - **Clone** your forked repository to your local machine using [Git](https://docs.github.com/en/get-started/getting-started-with-git/set-up-git) (make sure it's installed)

   ```bash
   git clone git@github.com:your-username/nexus-framework.git
   ```

4. **Install Dependencies**
   Navigate to the project directory and install any necessary dependencies. Ensure you have Go installed on your machine.

   ```bash
   cd nexus-framework
   go run main.go   
   ```

5. **Make Your Changes**
   After cloning and setting up your branch, make the necessary changes to the code in your IDE.

6. **Commit and Push**:
   Commit your changes and push them to your fork:

   ```bash
   git commit -m "Describe the changes you made"
   git push
   ```

   Alternatively, use VSCode's inbuilt Git source control pane `Ctrl+Shift+G` if you're unconfortable with a CLI


7. **Follow the right conventions**
    Use comments to explain your code.
    Adhere to the conventional commits format for commit messages (https://www.conventionalcommits.org/en/v1.0.0/#summary)

8. **Submit a Pull Request**:
   After pushing your changes, open a pull request to pull changes from your fork to the original repository.

9. **Get Feedback**
   Wait for a maintainer to review your pull request (PR) and provide feedback.

10. **Gain Bounty Points**
   If everything is approved, your issue will be closed, and you'll gain bounty points on the leaderboard!
