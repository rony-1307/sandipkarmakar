-- ============================================================
-- Database: Sandip Karmakar Portfolio / CV Data
-- Generated: 2026-08-23
-- ============================================================

CREATE DATABASE IF NOT EXISTS sandip_portfolio;
USE sandip_portfolio;

-- ------------------------------------------------------------
-- 1. PERSONAL DETAILS
-- ------------------------------------------------------------
CREATE TABLE personal_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    profile_image VARCHAR(255),
    page_background VARCHAR(255),
    logo VARCHAR(255),
    full_name VARCHAR(100) NOT NULL,
    current_designation VARCHAR(100) NOT NULL,
    current_department VARCHAR(100) NOT NULL,
	current_organization VARCHAR(100) NOT NULL,
    current_address VARCHAR(100) NOT NULL,
    gender VARCHAR(20),
    date_of_birth VARCHAR(50),
    home_address TEXT,
    phone1_ccode VARCHAR(10),
    phone1_no VARCHAR(20),
    phone2_ccode VARCHAR(10),
    phone2_no VARCHAR(20),
    email1 VARCHAR(150),
    email2 VARCHAR(150),
    portfolio_link VARCHAR(255),
    github_link VARCHAR(255),
    linkedin_link VARCHAR(255),
    google_scholar_link VARCHAR(255),
    orcid_link VARCHAR(255),
    researchgate_link VARCHAR(255),
    resume_link VARCHAR(255),
    father_name VARCHAR(100),
    mother_name VARCHAR(100),
    siblings INT,
    siblings_name VARCHAR(100),
    spouse_name VARCHAR(100)
);

INSERT INTO personal_details (
    profile_image, page_background, logo, full_name, current_designation, current_department,
    current_organization, current_address, gender, date_of_birth, home_address,
    phone1_ccode, phone1_no, phone2_ccode, phone2_no, email1, email2,
    portfolio_link, github_link, linkedin_link, google_scholar_link, orcid_link, researchgate_link,
    resume_link, father_name, mother_name, siblings, siblings_name, spouse_name
) VALUES (
    'static/images/hero-img/hero-img.png',
    'static/images/hero-bg/hero-bg.png',
    'static/images/logo/logo.png',
    'Sandip Karmakar',
    'PhD Scholar',
	'Electronics and Telecommunication Enginneering',
    'Jadavpur University (Main Campus)',
	'188, Raja S.C. Mallick Rd, Jadavpur, Kolkata, West Bengal 700032',
    'Male',
    '13th July 1994',
    'Konnagar, Hooghly,  West Bengal - 712235, [IN]',
    '+91',
    '8902085773',
    '+91',
    '7059446870',
    'skarmakar1307@gmail.com',
    'sandipk.etce.rs@jadavpuruniversity.in',
    'https://sandipkarmakar.onrender.com/',
    'https://github.com/rony-1307/',
    'https://www.linkedin.com/in/sandip-karmakar-a0239692/',
    'https://scholar.google.com/citations?hl=en&user=0YfIk6QAAAAJ/',
    'https://orcid.org/0009-0005-4616-4590',
    'https://www.researchgate.net/profile/Sandip-Karmakar-4?ev=hdr_xprf',
    'static/document/SandipKarmakar_Resume.pdf',
    'Swapan Karmakar',
    'Jharna Karmakar',
    1,
    'Sayantan Karmakar',
    'NA'
);
-- '77/42 Rammohan Place, PO: Konnagar, PS: Uttarpara, Dist: Hooghly, State: West Bengal, PIN: 712235, [IN]',
-- ------------------------------------------------------------
-- 1.1. HOBBIES
-- ------------------------------------------------------------
CREATE TABLE hobbies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    hobby VARCHAR(100)
);

INSERT INTO hobbies (hobby) VALUES
('Painting'),
('Swimming'),
('Bike Riding');

-- ------------------------------------------------------------
-- 1.2. LANGUAGES
-- ------------------------------------------------------------
CREATE TABLE languages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sl INT,
    language_name VARCHAR(50),
    proficiency VARCHAR(50),
    can_read BOOLEAN,
    can_write BOOLEAN,
    can_speak BOOLEAN
);

INSERT INTO languages (sl, language_name, proficiency, can_read, can_write, can_speak) VALUES
(1, 'Bengali', 'Native', TRUE, TRUE, TRUE),
(2, 'English', 'Advanced', TRUE, TRUE, TRUE),
(3, 'Hindi', 'Intermediate', TRUE, TRUE, TRUE);

-- ------------------------------------------------------------
-- 2. EDUCATION
-- ------------------------------------------------------------
CREATE TABLE education (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sl INT,
    level VARCHAR(50),
    degree VARCHAR(100),
    school_name VARCHAR(200),
    board_university VARCHAR(200),
    stream VARCHAR(255),
    start_date VARCHAR(50),
    end_date VARCHAR(50),
    year_of_passing VARCHAR(20),
    reg_num VARCHAR(100),
    roll_num VARCHAR(100),
    percentage_cgpa VARCHAR(50),
    thesis_title TEXT,
    supervisor VARCHAR(150),
    abstract TEXT,
    official_link VARCHAR(255),
    org_address TEXT
);

INSERT INTO education (sl, level, degree, school_name, board_university, stream, start_date, end_date, year_of_passing, reg_num, roll_num, percentage_cgpa, thesis_title, supervisor, abstract, official_link, org_address) VALUES
(6, 'Doctor of Philosophy', 'PhD', 'Jadavpur University', 'Jadavpur University',
 'Electronics and Telecommunication Engineering', '27/01/2026', 'Onging', NULL,
 '161220120018 of 2016 - 2017', '002330501013', 'NA (NA)',
 'Studies of Massive MIMO and RIS-Assisted NOMA IoT Networks for 5G and Beyond Networks',
 'Prof. (Dr.) Iti Saha Misra',
 'TBA',
 'https://jadavpuruniversity.in/',
 'Main Campus - 188 Raja Subodh Chandra Mullick Road, Jadavpur, Kolkata, West Bengal, PIN: 700047, [IN]'),

(5, 'Post Graduate', 'Master of Technology', 'Jadavpur University', 'Jadavpur University',
 'Distributed and Mobile Computing', '02/08/2023', '09/06/2025', '2025',
 '161220120018 of 2016 - 2017', '002330501013', '7.89 (71.40%)',
 'EMG Signal Acquisition and Transmission Over Low-Cost Lora Wireless System: Analysis for Fatigue Muscle',
 'Prof. (Dr.) Iti Saha Misra',
 'A vital instrument for measuring skeletal muscle electrical activity, electromyography (EMG) is used extensively in clinical diagnostics, sports science, and rehabilitation to track muscle exhaustion, which is a reduction in force production capability brought on by extended exercise. This thesis introduces a portable, affordable device that uses surface electromyography (sEMG) and LoRa wireless technology to assess muscle fatigue remotely. The system uses a Heltec LoRa 32 V2, an Arduino Uno, and an Advanced Technologies EMG Sensor V3.0 to record, analyze, and send EMG signals at 433 MHz over great distances (1–15 km) while using minimal power. Data capture (sampling EMG signals every 100 ms for 30 seconds), transmission over LoRa, and reception for viewing and analysis are its three stages of operation. To identify fatigue indicators such as MDF/MF shifts, RMS/MAV decreases, and increased signal variability, EMG signal analysis uses time domain (RMS, MAV, ZC, SSC, iEMG, variance, autocorrelation, waveform length), frequency domain (MF, MDF, PSD, PF, TP), time-frequency (STFT, WT, HHT), and nonlinear (SampEn, ApEn, Lyapunov, fractal dimension) techniques. Subjects'' pre, mid, and post-activity data show flattening curves with tiredness onset and increasing amplitude/frequency during activity. The method shows promise for real-time muscle monitoring in resource-constrained environments, such sports grounds and rural clinics, providing a cost-effective substitute for pricey commercial EMG equipment. This LoRa-based EMG system bridges the gap between state-of-the-art biomedical technology and accessibility by improving muscle fatigue analysis for performance enhancement, injury prevention, and rehabilitation.',
 'https://jadavpuruniversity.in/',
 'Second Campus - Plot No.8, Salt Lake Bypass, LB Block, Sector-III, Salt Lake City, Kolkata – 700106'),

(4, 'Graduate', 'Bachelor of Technology', 'St. Thomas'' College of Engineering and Technology', 'Maulana Abul Kalam Azad University of Technology',
 'Electronics and Communication Engineering', '15/09/2016', '19/07/2019', '2019',
 '161220120018 of 2016 - 2017', '12200316003', '7.05 (63.00%)',
 'Automatic Unauthorized Parking Detector with SMS Notification using IOT',
 'Dr. Dipankar Kundu',
 'Due to high population growth, car demand has increased at an alarming rate. This leads to increase in demand for more parking slots, which poses an acute problem, especially, when we are concerned with metro and fairly large cities. A solution to this problem on priority basis is necessary. People should have to cater to the illegal parking aspect as well. This paper deals with the detection of illegal parking and it also helps to identify the vehicles, which are parked in non-parking areas and send information regarding those vehicles to the control office. Thus it is meant for decreasing the number of illegal parking. A Raspberry Pi processor is the main device, which is able to manage the whole task. Advanced techniques of image processing, using Support Vector Machine (SVM) algorithm and Optical Character Recognition (OCR), have been used in the model.',
 'https://stcet.ac.in/',
 '4, Diamond Harbour Road, Kidderpore, Kolkata- 700023 West Bengal, [IN]'),

(3, 'Diploma', 'Diploma', 'Technique Polytechnic Institute', 'West Bengal State Council of Technical and Vocational Education and Skill Development',
 'Electronics and Tele-Communication Engineering', '08/08/2013', '24/08/2016', '2016',
 'D131479541 of 2013 - 2014', '53459', '7.7 (74.10%)',
 'Secured Wireless Real Time Electronic Voting Machine for Data Acquisition',
 'Subhadeep Chakraborty',
 'Electronic Voting Machine or EVM is generally used to count the poll result at the time of vote. In EVM generally a counting part is available where the counting are done and the count value is stored in the memory. In this paper, the design of the Wireless EVM has been proposed where the counting will be done in a remote section to avoid the fault or error caused by the several problems such as wrong button press, wrong counting, theft caused by the Stationary EVM. The data will be transferred from the EVM machine through a transmitter and this signal will be caught up by the receiver of the Counting module. The count will be shown at the display side as per preference that is the real time display can be turned off during the poll time. In this device, the voter cannot press the poll button of their preference twice as the device will be deactivated after single press. That is why the design proposed in this paper is of reduced error and works efficiently.',
 'https://www.techniqueedu.com/',
 'Vill.- Panchrokhi, P.O. Sugandhya, P.S. Polba, Dist. Hooghly, West Bengal, PIN- 712102, [IN]'),

(2, '12', 'Higher Secondary', 'Uttarpara Childrens'' Own Home', 'West Bengal Council of Higher Secondary Education',
 'Science (Beng, Eng, Chem, Math, Bios, Phys, Enve)', '26/04/2012', '31/05/2013', '2013',
 '2111080450 of 2011 - 2012', '211311 / 0470', '55%', NULL, NULL, NULL, NULL,
 '100 Rajendra Avenue, Kotrung, Uttarpara, Hooghly, West Bengal, PIN: 712258, [IN]'),
 
 (1, '10', 'Madhyamik', 'Uttarpara Amarendra Vidyapith', 'West Bengal Board of Secondary Education',
 'General (Beng, Eng, Math, Phy Sc, Life Sc, Hist, Geo)', '11/03/2010', '27/05/2011', '2011',
 '4101202017', 'D43661G / 0174', '60.625%', NULL, NULL, NULL, NULL,
 'BN Road, Bhadrakali Panchanantala Mandir, Kotrung, Uttarpara, Hooghly, West Bengal, PIN: 712232, [IN]');


-- ------------------------------------------------------------
-- 2. EXPERIENCE
-- ------------------------------------------------------------
CREATE TABLE experience (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sl INT,
    position VARCHAR(150),
    organization VARCHAR(200),
    department VARCHAR(200),
    date_of_joining VARCHAR(50),
    date_of_relieving VARCHAR(50),
    job_type VARCHAR(50),
    salary VARCHAR(50),
    responsibilities TEXT,
    other_responsibilities TEXT,
    org_link VARCHAR(255),
    org_add_main TEXT,
    org_add_secondary TEXT
);

INSERT INTO experience (sl, position, organization, department, date_of_joining, date_of_relieving, job_type, salary, responsibilities, other_responsibilities, org_link, org_add_main, org_add_secondary) VALUES
(2, 'Junior Research Fellow', 'Jadavpur University', 'Department of Electronics & Telecommunication Engineering', '04/09/2025', 'Ongoing', 'Contractual', '25000.00/- per month',
 'Design a Cost Effective Health Monitoring system under supervision of Prof. (Dr.) Iti Saha Misra a former Professor of Department of Electronics & Telecommunication Engineering at Jadavpur University',
 'None',
 'https://jadavpuruniversity.in/',
 '188 Raja Subodh Chandra Mullick Road, Jadavpur, Kolkata, West Bengal, PIN: 700047, [IN]',
 'Plot No.8, Salt Lake Bypass, LB Block, Sector-III, Salt Lake City, Kolkata, West Bengal, PIN: 700106, [IN]'),

(1, 'Lecturer', 'Salbani Institute of Technology', 'Department of Electrical Engineering', '03/02/2020', '12/05/2023', 'Permanent', '21000.00/- per month',
 'Delivered Lecture on Analog & Digital Electronics, Power Electronics, Microprocessor & Microcontroller, etc.',
 'Technical Person of Online CBT Examination, and work as LAN Installation, OS & Software Installation in Computer Lab, and other official job',
 'https://sitsalbani.org/',
 'Vill: Bankibandh, PO: Saiyedpur, PS: Salboni, Dist: Paschim Medinipur, State: West Bengal, PIN: 721147, [IN]',
 NULL);

-- ------------------------------------------------------------
-- 3. INDUSTRIAL TRAINING
-- ------------------------------------------------------------
CREATE TABLE industrial_training (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sl INT,
    topic VARCHAR(255),
    topic_display VARCHAR(255),
	topic_description TEXT,
    organization VARCHAR(200),
    org_address VARCHAR(255),
    start_date VARCHAR(50),
    end_date VARCHAR(50)
);

INSERT INTO industrial_training (sl, topic, topic_display, topic_description, organization, org_address, start_date, end_date) VALUES
(7, 'Introduction to IoT with AI-ML & Cloud Computing', 'static/images/indusTrain_display/indusTrain_7.png', 'Low data rate communication in IoT applications.', 'Indian Institute of Technology - Kharagpur', 'Kharagpur, Paschim Medinipur, West Bengal', 'February 2025', 'August 2025'),
(6, 'Advance Data Science & Machine Learning', 'static/images/indusTrain_display/indusTrain_6.png', 'Advanced concepts in data science and machine learning.', 'Topstack', 'Chandan Nagar, Hooghly, West Bengal', 'July 2023', 'February 2024'),
(5, 'FPGA based VLSI Design', 'static/images/indusTrain_display/indusTrain_5.png', 'Learning about the fundamentals of FPGA-based VLSI design.', 'Sandeepani School of Embedded System Design', 'Koramangala, Bangalore, Karnataka', 'February 2025', 'August 2025'),
(4, 'Advance Java and Java Spring Framework', 'static/images/indusTrain_display/indusTrain_4.png', 'Learning about the fundamentals of Java and Spring Framework development.', 'Topstack', 'Chandan Nagar, Hooghly, West Bengal', 'March 2022', 'July 2022'),
(3, 'HTML, CSS, JAVA Script, Node JS, Mongo DB', 'static/images/indusTrain_display/indusTrain_3.png', 'Learning about the fundamentals of web development and database management.', 'Topstack', 'Chandan Nagar, Hooghly, West Bengal', 'August 2021', 'December 2021'),
(2, 'Industrial Electronics, PLC, Microcontroller', 'static/images/indusTrain_display/indusTrain_2.png', 'Learning about the fundamentals of industrial electronics, PLC, and microcontroller applications.', 'G.E. Motors (Pvt.) Ltd', 'Sheoraphuli, Hooghly, West Bengal', '07/06/2018', '23/06/2018'),
(1, 'Basic Television Transmission System', 'static/images/indusTrain_display/indusTrain_1.png', 'Learning about the fundamentals of television transmission and broadcasting.', 'Praser Bharati, Doordarshan Kendra', 'Kolkata, West Bengal', '12/10/2015', '16/10/2015');



-- ------------------------------------------------------------
-- 4. PUBLICATIONS (Conference / Journal / Patent / Book)
-- ------------------------------------------------------------
CREATE TABLE publications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sl INT,
    pub_type ENUM('Book', 'Conference', 'Journal', 'Patent') NOT NULL,
    title TEXT,
    authors TEXT,
    venue VARCHAR(255),
    doi VARCHAR(150),
    status VARCHAR(50),
    link VARCHAR(255)
);

INSERT INTO publications (sl, pub_type, title, authors, venue, doi, status, link) VALUES
(1, 'Book', 'TBA',
 'TBA',
 'TBA',
 'TBA', 'TBA',
 'TBA'),

(2, 'Conference', 'A Portable IoT-Integrated Pulse Oximeter Like Blood Glucose Prediction Model in Normoglycemic Range',
 'Sandip Karmakar, Suman Paria, Iti Saha Misra',
 'CALCON 2026, IEEE', 'TBA', 'Under Review', 'TBA'),

(1, 'Conference', 'Development of an IoT-Driven Wireless Smart Health Care System for Continuous Heart Monitoring',
 'Suman Paria; Sandip Karmakar; Iti Saha Misra',
 '2025 Devices for Integrated Circuit (DevIC), 5-6 April, 2025, Kalyani, India | 979-8-3503-9110-7/25/$31.00 ©2025 IEEE',
 '10.1109/DevIC63749.2025.11012139', 'Published',
 'https://ieeexplore.ieee.org/document/11012139'),

(3, 'Journal', 'Reliable LoRa P2P Indoor and Outdoor IoT Health Data Transmission: Entropy and Spectral based Approach',
 'Suman Paria, Iti Saha Misra, Sandip Karmakar',
 'Wiley Journal of Wireless Communications and Mobile Computing, 2026',
 'TBA', 'Under Review', NULL),

(2, 'Journal', 'Automatic Unauthorized Parking Detector with SMS Notification',
 'Madhurima Chakrabarti, Sandip Karmakar, Sumit Singh, Madhura Sur, Dipankar Kundu',
 'International Advanced Research Journal in Science, Engineering and Technology, Vol. 6, Issue 5, May 2019',
 '10.17148/IARJSET.2019.6522', 'Published',
 'https://iarjset.com/papers/automatic-unauthorized-parking-detector-with-sms-notification/'),

(1, 'Journal', 'Design of Secured Wireless Real Time Electronic Voting Machine',
 'Subhadeep Chakraborty, Sandip Karmakar, Rima Jana, Subhradeep Dey',
 'International Journal of Innovative Research in Electrical, Electronics, Instrumentation and Control Engineering, Vol. 3, Issue 9, September 2015',
 '10.17148/IJIREEICE.2015.3922', 'Published',
 'https://ijireeice.com/papers/design-of-secured-wireless-real-time-electronic-voting-machine/'),

(1, 'Patent', 'TBA',
 'TBA',
 'TBA',
 'TBA', 'TBA',
 'TBA');

-- ------------------------------------------------------------
-- 5. PROJECTS
-- ------------------------------------------------------------
CREATE TABLE projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sl INT,
    title VARCHAR(255),
    proj_display VARCHAR(255),
    supervisor VARCHAR(150),
    abstract TEXT,
    tools TEXT,
	status VARCHAR(50),
    start_date VARCHAR(50),
    end_date VARCHAR(50)
);

INSERT INTO projects (sl, title, proj_display, supervisor, abstract, tools, status, start_date, end_date) VALUES
(8, 'Cost Effective Design and Implementation of Health Companion System for Human Bio-Signal Acquisition and Remote Monitoring in Rural/Urban Region: An IoT Prototype Model',
 'static/images/proj_display/proj8.png',
 'Prof. (Dr.) Iti Saha Misra',
 'TBA',
 'Arduino Uno, Heltec WiFi LoRa 32 V3, Advanced Technology EMG Sensor, Arduino IDE, Python Programming Language',
 'Ongoing', '04/09/2025', 'Ongoing'),

(7, 'EMG Signal Acquisition and Transmission Over Low-Cost LoRa Wireless System: Analysis for Fatigue Muscle',
 'static/images/proj_display/proj7.png',
 'Prof. (Dr.) Iti Saha Misra',
 'A vital instrument for measuring skeletal muscle electrical activity, electromyography (EMG) is used extensively in clinical diagnostics, sports science, and rehabilitation to track muscle exhaustion, which is a reduction in force production capability brought on by extended exercise. This thesis introduces a portable, affordable device that uses surface electromyography (sEMG) and LoRa wireless technology to assess muscle fatigue remotely. The system uses a Heltec LoRa 32 V2, an Arduino Uno, and an Advanced Technologies EMG Sensor V3.0 to record, analyze, and send EMG signals at 433 MHz over great distances (1–15 km) while using minimal power. Data capture (sampling EMG signals every 100 ms for 30 seconds), transmission over LoRa, and reception for viewing and analysis are its three stages of operation. To identify fatigue indicators such as MDF/MF shifts, RMS/MAV decreases, and increased signal variability, EMG signal analysis uses time domain (RMS, MAV, ZC, SSC, iEMG, variance, autocorrelation, waveform length), frequency domain (MF, MDF, PSD, PF, TP), time-frequency (STFT, WT, HHT), and nonlinear (SampEn, ApEn, Lyapunov, fractal dimension) techniques. Subjects'' pre, mid, and post-activity data show flattening curves with tiredness onset and increasing amplitude/frequency during activity. The method shows promise for real-time muscle monitoring in resource-constrained environments, such sports grounds and rural clinics, providing a cost-effective substitute for pricey commercial EMG equipment. This LoRa-based EMG system bridges the gap between state-of-the-art biomedical technology and accessibility by improving muscle fatigue analysis for performance enhancement, injury prevention, and rehabilitation.',
 'Arduino Uno, Heltec WiFi LoRa 32 V3, Advanced Technology EMG Sensor, Arduino IDE, Python Programming Language',
 'Complete', '02/05/2024', '09/06/2025'),

(6, 'Development of an IoT-Driven Wireless Smart Health Care System for Continuous Heart Monitoring',
 'static/images/proj_display/proj6.png',
 'Prof. (Dr.) Iti Saha Misra',
 'The swift development of IoT driven Telemedicine for the continuous remote monitoring of patients have motivated to use Message Queuing Telemetry Transport (MQTT) protocol with a Motorized Hand-Cuff type BP Machine, a LoRa enable ESP32 and Raspberry Pi 5 to design an efficient, real time heart monitoring system. The total cardiac health condition was acquired as BP and Heart Rate and transmitted to another location by means of Wireless Communication using a widely used light weight MQTT protocol for our application. The health data was acquired using an affordable and energy efficient LoRa with low-cost sensors and the MQTT protocol was deployed using LoRa and Raspberry pi.',
 'Heltec WiFi LoRa 32 V3, Raspberry Pi 5, MQTT Protocol, LAN',
 'Complete', '06/09/2024', '30/01/2025'),

(5, 'Design SPI Protocol',
 'static/images/proj_display/proj5.png',
 'Sandeepani School of Embedded System Design Koramangala, Bangalore, Karnataka',
 'we design this project in Verilog code in Vivado platform. SPI (Serial Peripheral Interface) Protocol, it is a communication between Master and Slave, Master and Slave communicate through MOSI (Master Out Slave In) and MISO (Master Out Slave In), there have four mode it is working on the signal of CPOL and CPHA',
 'Vivado Programming Platform, Verilog Programming, ZED Board',
 'Complete', '06/06/2022', '05/07/2022'),

(4, 'Automatic Unauthorized Parking Detector with SMS Notification using IOT',
 'static/images/proj_display/proj4.png',
 'Dr. Dipankar Kundu',
 'Due to high population growth, car demand has increased at an alarming rate. This leads to increase in demand for more parking slots, which poses an acute problem, especially, when we are concerned with metro and fairly large cities. A solution to this problem on priority basis is necessary. People should have to cater to the illegal parking aspect as well. This paper deals with the detection of illegal parking and it also helps to identify the vehicles, which are parked in non-parking areas and send information regarding those vehicles to the control office. Thus it is meant for decreasing the number of illegal parking. A Raspberry Pi processor is the main device, which is able to manage the whole task. Advanced techniques of image processing, using Support Vector Machine (SVM) algorithm and Optical Character Recognition (OCR), have been used in the model.',
 'Raspberry Pi 3B+, Python Programming Language, SVM Classifier, OpenCV, Image Processing',
 'Complete', 'August 2018', 'May 2019'),

(3, 'Wi-Fi Controlled Robo Car', 'static/images/proj_display/proj3.png', NULL, 'TBA', 'NodeMCU, Arduino Uno, Arduino IDE C Programming', 'Complete', 'February 2018', 'March 2018'),

(2, 'Design of Secured Wireless Real Time Electronic Voting Machine for Data Acquisition',
 'static/images/proj_display/proj2.png',
 'Subhadeep Chakrabarti',
 'Electronic Voting Machine or EVM is generally used to count the poll result at the time of vote. In EVM generally a counting part is available where the counting are done and the count value is stored in the memory. In this paper, the design of the Wireless EVM has been proposed where the counting will be done in a remote section to avoid the fault or error caused by the several problems such as wrong button press, wrong counting, theft caused by the Stationary EVM. The data will be transferred from the EVM machine through a transmitter and this signal will be caught up by the receiver of the Counting module. The count will be shown at the display side as per preference that is the real time display can be turned off during the poll time. In this device, the voter cannot press the poll button of their preference twice as the device will be deactivated after single press. That is why the design proposed in this paper is of reduced error and works efficiently.',
 'Microcontroller AT89C51, Keil C Programming language',
 'Complete', 'August 2015', 'May 2016'),

(1, 'Automatic Street Light Control', 'static/images/proj_display/proj1.png', NULL, 'TBA', 'PIR Motion Sensor, High gain Transistor', 'Complete', 'August 2015', 'September 2015');

-- ------------------------------------------------------------
-- 6. ACHIEVEMENTS
-- ------------------------------------------------------------
CREATE TABLE achievements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    sl INT,
    title VARCHAR(255),
    category VARCHAR(100),          -- e.g. Exam, Position, Publication, Teaching, Training
    status VARCHAR(50),             -- Qualified, Ongoing, Completed, Published, Accepted
    description TEXT,
    organization VARCHAR(255),
    location VARCHAR(255),
    start_date VARCHAR(50),
    end_date VARCHAR(50),
    link VARCHAR(255)
);

INSERT INTO achievements (sl, title, category, status, description, organization, location, start_date, end_date, link) VALUES
(1, 'UGC NET Qualified', 'Exam', 'Qualified',
 'Successfully cleared the UGC National Eligibility Test (NET) in June 2025. This qualification makes me eligible for the post of Assistant Professor and/or Junior Research Fellowship (JRF) in Indian universities and colleges.',
 'University Grants Commission (UGC)', 'India', 'June 2025', 'June 2025', NULL),

(2, 'Junior Research Fellow', 'Position', 'Ongoing',
 'Working as Junior Research Fellow at Jadavpur University on the design of a cost-effective IoT-based health monitoring system under the supervision of Prof. (Dr.) Iti Saha Misra.',
 'Jadavpur University', 'Kolkata, West Bengal, India', '04/09/2025', 'Ongoing', 'https://jadavpuruniversity.in/'),

(3, 'IEEE Conference Paper Published', 'Publication', 'Published',
 'Paper titled "Development of an IoT-Driven Wireless Smart Health Care System for Continuous Heart Monitoring" published in 2025 Devices for Integrated Circuit (DevIC), IEEE.',
 'IEEE DevIC 2025', 'Kalyani, India', 'April 2025', 'April 2025', 'https://ieeexplore.ieee.org/document/11012139'),

(4, 'Lecturer', 'Teaching', 'Completed',
 'Served as Lecturer in the Department of Electrical Engineering. Taught Analog & Digital Electronics, Power Electronics, Microprocessor & Microcontroller, and handled laboratory & official responsibilities.',
 'Salbani Institute of Technology', 'Paschim Medinipur, West Bengal, India', '03/02/2020', '12/05/2023', 'https://sitsalbani.org/'),

(5, 'Industrial Training – IoT with AI-ML & Cloud Computing', 'Training', 'Completed',
 'Completed industrial training on Introduction to IoT with AI-ML & Cloud Computing.',
 'Indian Institute of Technology – Kharagpur', 'Kharagpur, West Bengal, India', 'February 2025', 'August 2025', NULL);

-- ============================================================
-- END OF DATA
-- ============================================================