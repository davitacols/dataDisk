Contributing to DataDisk
========================

We're thrilled that you're interested in contributing to DataDisk! Your contributions help us make it a better tool for everyone. This guide walks you through the process of making a contribution.

.. contents::
   :local:

Getting Started
===============

Create a Branch
---------------

Start by creating a new branch in your local repository to house your changes. Use a descriptive name like `feature/enhanced-search` or `bugfix/login-issue`:

.. code-block:: bash

   git checkout -b feature/your-contribution

Make Your Changes
-----------------

Implement your code changes, documentation updates, or other contributions within this branch.

Commit Your Work
----------------

Commit your changes with clear and concise commit messages that explain the purpose of the changes:

.. code-block:: bash

   git add .
   git commit -m "Implemented feature to handle X"

Push to Your Fork
-----------------

Push your branch to your forked repository on GitHub:

.. code-block:: bash

   git push origin feature/your-contribution

Open a Pull Request
--------------------

Create a pull request on GitHub, requesting to merge your branch into the main branch of the original DataDisk repository.

Reporting Issues
================

If you encounter a bug or have a suggestion for improvement, please open an issue on the project's issue tracker. When reporting an issue:

- Provide a clear and concise description of the problem.
- Describe the steps to reproduce the issue (if applicable).
- Specify your system information, including operating system, Python version, and relevant libraries.

Code Style
==========

To maintain consistency, please adhere to the existing code style and conventions used in the project. Refer to the project's style guide for specific guidelines.

Testing
=======

Ensure that your changes don't inadvertently break existing functionality. If you're adding new features, consider writing tests to ensure their correctness. To run tests locally:

.. code-block:: bash

   python -m unittest discover tests

Collaboration and Support
=========================

We value your contributions and are here to help! If you have any questions or need assistance during the contribution process, feel free to reach out to the community or core developers.

Thank you for your interest in making DataDisk better!
