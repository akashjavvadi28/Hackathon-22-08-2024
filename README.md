# Electronic Voting System

## Overview

The Electronic Voting System is a console-based application designed to facilitate a secure and transparent voting process. It allows voters to register, cast their votes, and allows officials to manage the voting process, including scheduling, counting votes, and managing candidates and voters.

## Features

- **Voter Registration**: Allows voters to register by providing their full name, age, and ID proof (e.g., Aadhar, Passport, Driving License).
- **Candidate Nomination**: Candidates can nominate themselves by providing their details, including the position they are running for.
- **Vote Casting**: Registered voters can cast their votes for nominated candidates.
- **Official Panel**: Accessible by officials for managing the voting process, including:
  - Counting votes
  - Deleting or blocking candidates and voters
  - Enabling or disabling voting
  - Scheduling the voting period

## Requirements

- Python 3.x
- `cryptography` library (for secure handling of credentials and votes, if required)
