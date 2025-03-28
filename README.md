# CircuitBreak: Smart City Traffic Simulation

**CircuitBreak** is a simulation of smart city traffic systems, where cars move across roads, follow traffic lights, and obey traffic rules. The project leverages Pygame for visualization and simulates dynamic road networks with traffic lights and vehicle movements.

![image](https://github.com/user-attachments/assets/25a396c2-9cf8-4c85-a224-6f89422ccdd9)

---

## Features

- **Smart Traffic Control**: Simulates traffic lights at intersections with green and red phases, affecting car movement.
- **Random Car Generation**: Cars are randomly spawned on roads and can move in four directions (North, South, East, West).
- **Grid-Based Road Layout**: A dynamic 17x17 grid where roads and intersections are created.
- **Car Movement Logic**: Cars move along roads, stop at red lights, and obey traffic rules.

---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/circuitbreak.git
    cd circuitbreak
    ```

2. Install dependencies:

    ```bash
    pip install pygame
    ```

---

## Usage

To start the simulation:

1. Run the `main.py` script.

    ```bash
    python main.py
    ```

2. The simulation window will open, showing a grid-based city with roads and cars moving according to traffic lights.

---

## Controls

- **Escape**: Exit the simulation.
- **P**: Pause the simulation.

---

## Cyber Attack Considerations

As **CircuitBreak** simulates traffic control within a smart city, it's important to consider the vulnerability of such systems to cyber attacks. In a real-world scenario, smart traffic management systems could be a target for malicious actors aiming to disrupt city infrastructure. Possible attack vectors include:

- **Traffic Light Manipulation**: Attackers could change traffic light timings to cause congestion or accidents.
- **Car Hijacking**: Remote takeover of autonomous vehicles within the grid could lead to chaos and safety hazards.
- **Denial of Service (DoS)**: Overloading the system with excessive traffic requests, causing delays or system failure.

In future versions of this simulation, I plan to integrate cybersecurity mechanisms to:

- **Simulate and Respond to Cyber Threats**: Adding features where the simulation detects and responds to potential cyber threats.
- **Secure Traffic Light Communication**: Implementing encrypted communication channels for traffic lights to prevent unauthorized manipulation.
- **Vehicle Security**: Enabling basic vehicle-level security mechanisms to prevent unauthorized access or control.

---

## Future Plans

- Add more realistic traffic behavior and flow.
- Improve car AI for better traffic management.
- Include more interactive features such as manual control over traffic lights.
- Implement security measures to prevent cyber attacks in future updates.

---

## Contributing

Feel free to fork this project, open issues, or submit pull requests for improvements. Contributions are welcome!

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
