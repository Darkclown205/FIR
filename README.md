# Online FIR System

## Project Overview
The Online FIR System is a web application that allows users to file First Information Reports (FIRs) online and enables authorities to manage and track these reports efficiently. The system provides an easy-to-use interface for users to submit FIRs, upload evidence, and receive updates on their cases. Authorities, such as police officers, can view, search, and manage FIRs, including updating their status and downloading evidence.

## Video Demonstration
A video demonstration of the project can be viewed at: [Your Video URL Here]

## Key Features
- **User Registration & Authentication**: Users can register and log in to the system. Different roles (user, cops) have different access levels and functionalities.
- **FIR Submission**: Users can submit FIRs by providing details such as the title, description, location, and action requested. They can also upload supporting evidence.
- **FIR Management**: Authorized personnel (cops) can view, search, and update the status of FIRs. They can also download evidence attached to the FIRs.
- **Secure and Efficient**: The system ensures that only authorized users can access and manage FIR data.

## Technology Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **Data Storage**: JSON files for storing user and FIR data

## Installation & Usage
1. **Clone the repository**: 
    ```
    git clone [https://github.com/Darkclown205/FIR]
    ```
2. **Navigate to the project directory**:
    ```
    cd [Project Directory]
    ```
3. **Install the required packages**:
    ```
    pip install -r requirements.txt
    ```
4. **Run the Streamlit application**:
    ```
    streamlit run app.py
    ```

## Future Improvements
- **Email Notifications**: Integrate email notifications for users to receive updates on their FIR status.
- **Database Integration**: Transition from JSON files to a more robust database system.
- **Role-based Access Control**: Implement finer control over user permissions and access to sensitive data.

## Acknowledgments
This project was developed as part of the CS50 course. Special thanks to the course instructors and community for their support and guidance.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
