# Data Center Architecture & Load Profiling Specification Document

This document provides an exhaustive technical breakdown of Architecture and Load Profiling responsibilities, vocabulary, architecture models, algorithmic logic, and Software Development Life Cycle (SDLC) documentation for the **SPE AMTS Energython 2026** techno-economic project.

## 1. Role Definition and Core Accountabilities

 When carrying out **Data Center Architecture & Load Profiling**, the primary mandate is to design the computational infrastructure, model total IT energy demand profiles, benchmark tropical thermal performance, and build the real-time software engine that orchestrates power-aware compute workloads.

```
                     +---------------------------------------+
                     |        Computer Scientist #1          |
                     | Architecture & Telemetry Control Engine|
                     +-------------------+-------------------+
                                         |
         +-------------------------------+-------------------------------+
         |                               |                               |
         v                               v                               v
+------------------+           +------------------+            +------------------+
| IT Infrastructure|           | Workload Profiling|            | Real-Time PUE    |
|   Sizing Model   |           |  & Load Curves   |            |   Optimization   |
+--------+---------+           +--------+---------+            +--------+---------+
         |                              |                               |
         +-------------------------------+-------------------------------+
                                         |
                                         v
                     +---------------------------------------+
                     | Hourly Power Demand Profile (MW Stream)|
                     +-------------------+-------------------+
                                         |
         +-------------------------------+-------------------------------+
         |                               |                               |
         v                               v                               v
+------------------+           +------------------+            +------------------+
| Electrical Eng.  |           | Mechanical Eng.  |            | Comp. Scientist 2|
| (Gen. Capacity)  |           | (Cooling Loops)  |            | (Financial Model)|
+------------------+           +------------------+            +------------------+
```

### Key Functional Responsibilities:

1. **IT Infrastructure Sizing**: Dimension server density, compute rack distributions, and rack power allocations (20 kW to 100+ kW per rack) to align strictly with the target facility capacity ceiling of 10–20 MW.

2. **Load Demand Profiling**: Construct high-resolution (1-minute to hourly) temporal power consumption curves reflecting baseline idle draw, peak compute bursts, and diurnal fluctuations across artificial intelligence (AI) training/inference workloads and cloud enterprise tasks.

3. **Tropical PUE Benchmarking**: Analyze thermodynamic power overheads in high-ambient temperature/humidity regions (e.g., Nigeria, Kenya, Egypt) to set realistic Power Usage Effectiveness ($PUE$) baselines.

4. **Telemetry & Orchestration Software**: Architect the Data Center Infrastructure Management (DCIM) telemetry pipeline, ingestion database schemas, closed-loop thermal feedback algorithms, and energy-aware workload scheduling software.

## 2. Terminology and Technical Vocabulary Dictionary

The following are the few terminologies that will enable easy comprehension and syncing of the development teams for easy collaboration.

| **Vocabulary Term**                              | **Technical Definition**                                                                                               | **Operational Relevance**                                                                       |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **PUE (Power Usage Effectiveness)**              | The ratio of total facility power entering the building boundary to the power delivered to IT equipment.               | Core KPI for measuring electrical and thermal overhead efficiency.                              |
| **DCiE (Data Center Infrastructure Efficiency)** | The mathematical reciprocal of PUE expressed as a percentage: $DCiE = \left( \frac{1}{PUE} \right) \times 100\%$.      | Measures the direct percentage of incoming power reaching compute nodes.                        |
| **Rack Power Density (kW/rack)**                 | The electrical power consumed by hardware mounted within a standardized 42U/48U IT rack.                               | Dictates cooling infrastructure topology (air-cooled vs. direct-to-chip vs. immersion cooling). |
| **Diurnal Load Curve**                           | Time-series representation of electrical demand over a 24-hour cycle showing peak operational shifts.                  | Enables dynamic generator throttles and contractual take-or-pay fuel alignment.                 |
| **DCIM Telemetry Engine**                        | Software platform aggregating high-frequency sensor streams (Modbus, BACnet, SNMP) across electrical and thermal gear. | Central monitoring hub developed by CS #1 to record real-time facility operational state.       |
| **Category 2 PDU Measurement Tap**               | PUE reporting methodology measuring IT energy directly at the Intelligent Power Distribution Unit output tap.          | Prevents downstream transformer conversion losses from inflating compute power metrics.         |
| **Take-or-Pay Fuel Alignment**                   | Software scheduling logic that adjusts compute job execution to maintain fuel draw above contractual minimums.         | Prevents financial penalties caused by under-consuming contracted natural gas volumes.          |
| **Time-Series Hypertable**                       | Optimized database table partitioned by time intervals to process high-throughput sensor telemetry.                    | Underlying database structure (TimescaleDB) used to store multi-year operational metrics.       |
| **PID Closed-Loop Control**                      | Proportional-Integral-Derivative feedback algorithm adjusting physical actuation based on system error deltas.         | Controls variable-frequency drive (VFD) pumps and fans based on real-time PUE drifts.           |
| **Edge Compute Orchestration**                   | Decentralized scheduling software managing workloads across localized modular data center pods.                        | Coordinates hybrid compute nodes distributed between main facility halls and edge sites.        |

## 3. IT Infrastructure Sizing and Compute Topology

The first role is to establish the physical and electrical topology of the IT compute assets to match the target 10–20 MW gross generation limit.

### 3.1 Compute Sizing Methodology (15 MW Baseline Case)

Assuming a target baseline generation of $15\text{ MW}$ gross facility power and an estimated tropical design $PUE$ of $1.25$ using hybrid liquid cooling:

$$\text{Max IT Compute Load } (E_{\text{IT}}) = \frac{E_{\text{Total}}}{PUE} = \frac{15.0\text{ MW}}{1.25} = 12.0\text{ MW}$$

### 3.2 Rack Density Allocation Profile

To support heterogeneous workloads (Enterprise Cloud, High-Performance Computing, and AI Large Language Model Training), compute halls are partitioned into three density tiers:

```
+---------------------------------------------------------------------------------+
|                         TOTAL IT CAPACITY: 12.0 MW                              |
+---------------------------------------------------------------------------------+
|  Zone A: Standard Cloud      |  Zone B: High-Density HPC   |  Zone C: AI Immersion |
|  5.0 MW Net IT               |  4.0 MW Net IT              |  3.0 MW Net IT        |
|  250 Racks @ 20 kW/rack      |  80 Racks @ 50 kW/rack      |  30 Racks @ 100 kW/rack|
|  Air / Rear-Door Cooling     |  Direct-to-Chip Liquid      |  Single-Phase Immersion|
+------------------------------+-----------------------------+--------------------+
```

| **Hall Zone** | **Workload Target**              | **Power Density** | **Rack Count** | **Aggregate Zone IT Draw**   | **Primary Cooling Topology**                              |
| ------------- | -------------------------------- | ----------------- | -------------- | ---------------------------- | --------------------------------------------------------- |
| **Zone A**    | General Enterprise Cloud / SaaS  | 20 kW / rack      | 250 Racks      | 5.0 MW                       | Hot/Cold Aisle Containment + Chilled Water CRAC           |
| **Zone B**    | High-Performance Computing (HPC) | 50 kW / rack      | 80 Racks       | 4.0 MW                       | Direct-to-Chip (D2C) Cold Plate Liquid Cooling            |
| **Zone C**    | AI LLM Training & Deep Learning  | 100 kW / rack     | 30 Racks       | 3.0 MW                       | Single-Phase / Two-Phase Immersion Cooling Tanks          |
| **Total**     | **Combined Compute Estate**      | **Varies**        | **360 Racks**  | **12.0 MW IT (15 MW Gross)** | **Hybrid Thermal Architecture**<br><br> <br><br>[cite: 2] |

## 4. Workload Profiling and Energy Demand Modeling

Compute loads are dynamic, varying by hour, day, and processing task. Therefore we construct synthetic and empirical load profiles to model total facility demand.

### 4.1 Workload Power Breakdown Mechanics

The power consumption of an individual server rack ($P_{\text{Rack}}$) is modeled as a function of component state:

$$P_{\text{Rack}} = N_{\text{Server}} \times \Big[ P_{\text{Idle}} + U_{\text{CPU}} (P_{\text{CPU\_Max}} - P_{\text{Idle}}) + U_{\text{GPU}} (P_{\text{GPU\_Max}} - P_{\text{Idle}}) + P_{\text{Memory}} + P_{\text{Fans}} \Big]$$

Where:

- $N_{\text{Server}}$ = Number of active servers per rack.

- $P_{\text{Idle}}$ = Baseline idle power draw (typically 30%–40% of max power).

- $U_{\text{CPU}}, U_{\text{GPU}}$ = Real-time utilization percentages ($0.0$ to $1.0$).

### 4.2 Diurnal Profile Generation (24-Hour Cycle)

```
        Typical 24-Hour IT Compute Load & Facility Demand (15 MW Facility)
  16 MW +-------------------------------------------------------------------+
        |                                       --- Total Facility (PUE 1.25)|
  14 MW |                       + + + + + + + +                              |
        |                     +                 +                            |
  12 MW |=== === === === === +                   + === === === === === === ==| <--- Peak IT Load (12 MW)
        |                   +                     +                          |
  10 MW |                  +                       +                         |
        |  ----------------                         ------------------------ | <--- Cloud Base (8 MW)
   8 MW | |                |                       |                        |
        +------------------+-----------------------+------------------------+
        00:00            06:00                   12:00                    23:59
        [--- Off-Peak Batch ---]  [--- Peak Enterprise ---]  [--- Night Batch ---]
```

- **Off-Peak Night Window (00:00 - 06:00)**: Interactive cloud traffic drops to baseline ($8.0\text{ MW}$ IT load). Automated batch AI model retraining jobs fill available overhead up to $11.5\text{ MW}$ IT load to maintain gas engine generator baseline efficiency.

- **Peak Business Window (08:00 - 17:00)**: Enterprise SaaS, API calls, and regional cloud traffic peak ($12.0\text{ MW}$ IT load). Non-urgent background jobs are programmatically throttled or deferred.

- **Evening Shift Window (18:00 - 23:59)**: Digital media streaming and consumer mobile traffic rise; AI batch queues resume execution.

## 5. Tropical PUE Benchmarking and Thermal Mathematics

Operating data center infrastructure across tropical growth hubs (e.g., Lagos, Nairobi, Cairo) introduces extreme ambient dry-bulb temperatures ($35^\circ\text{C}$ to $42^\circ\text{C}$) and high relative humidity. Traditional air-chilled facilities struggle, often yielding poor $PUE$ ratios between $1.60$ and $1.80$.

### 5.1 Comprehensive Energy and Efficiency Equations

The foundational energy efficiency of the compute ecosystem is evaluated using four primary mathematical formulas:

1. **Power Usage Effectiveness ($PUE$)**:

   $$PUE = \frac{E_{\text{Total}}}{E_{\text{IT}}} = \frac{E_{\text{IT}} + E_{\text{Cooling}} + E_{\text{Electrical\_Losses}} + E_{\text{Auxiliary}}}{E_{\text{IT}}}$$

2. **Data Center Infrastructure Efficiency ($DCiE$)**:

   $$DCiE = \frac{1}{PUE} \times 100\% = \left( \frac{E_{\text{IT}}}{E_{\text{Total}}} \right) \times 100\%$$

3. **Infrastructure Overhead Ratio**:

   $$\text{Overhead Ratio} = PUE - 1 = \frac{E_{\text{Cooling}} + E_{\text{Electrical\_Losses}} + E_{\text{Auxiliary}}}{E_{\text{IT}}}$$

4. **Cooling Mass Flow Rate Heat Transfer Formula**:

   $$Q_{\text{thermal}} = \dot{m} \cdot C_p \cdot (T_{\text{Return}} - T_{\text{Supply}})$$

### 5.2 Comparative Cooling Efficiency Matrix

| **Cooling Technology**                 | **Typical Tropical PUE Target** | **Overhead Ratio (PUE−1)** | **DCiE (%)**  | **Water Usage Impact**                       | **Climate Suitability**                        |
| -------------------------------------- | ------------------------------- | -------------------------- | ------------- | -------------------------------------------- | ---------------------------------------------- |
| **Legacy DX Air Cooling**              | 1.65 – 1.80                     | 0.65 – 0.80                | 55.5% – 60.6% | Low direct water use; high power draw.       | Poor in high ambient heat.                     |
| **Chilled Water + Evaporative Towers** | 1.35 – 1.45                     | 0.35 – 0.45                | 68.9% – 74.0% | Severe water consumption (evaporative loss). | Constrained by regional water scarcity.        |
| **Direct-to-Chip (D2C) Liquid**        | 1.18 – 1.25                     | 0.18 – 0.25                | 80.0% – 84.7% | Minimal closed-loop fluid loss.              | Highly efficient for high-density racks.       |
| **Single-Phase Liquid Immersion**      | 1.08 – 1.15                     | 0.08 – 0.15                | 86.9% – 92.5% | Zero water loss (dielectric fluid).          | Ideal for extreme tropical ambient conditions. |

## 6. Complete Software Development Life Cycle (SDLC) Documentation

At this point we design, build, test, and deploy the **Data Center Control and Infrastructure Management Engine (DCIM-Engine)** through a structured five-phase SDLC framework.

```
+---------------------------------------------------------------------------------+
|                       SOFTWARE DEVELOPMENT LIFE CYCLE (SDLC)                    |
+---------------------------------------------------------------------------------+
| Phase 1: Requirements Gathering & Microservices System Architecture             |
| Phase 2: Algorithmic Engineering (PID PUE Control & Take-or-Pay Balancing)     |
| Phase 3: Infrastructure Integration, Telemetry Drivers & Database Schemas       |
| Phase 4: Verification, Chaos Engineering & Hardware-in-the-Loop Testing         |
| Phase 5: Production Deployment, Monitoring & Model Maintenance Retraining       |
+---------------------------------------------------------------------------------+
```

### Phase 1: Requirements Gathering and Architecture Design

The DCIM-Engine utilizes an event-driven microservices architecture built over an Apache Kafka event streaming bus. Microservices are isolated into dedicated containers running on an edge Kubernetes cluster located within the facility.

```
                    PHYSICAL HARDWARE LAYER
   +-------------------+  +-------------------+  +-------------------+
   | Switchgear Meters |  | Intelligent PDUs  |  | Immersion Sensors |
   +---------+---------+  +---------+---------+  +---------+---------+
             | Modbus TCP           | SNMP v3              | BACnet IP
             v                      v                      v
   +-----------------------------------------------------------------+
   |                     Ingestion Edge Gateways                     |
   +--------------------------------+--------------------------------+
                                    | JSON Telemetry Stream
                                    v
   +-----------------------------------------------------------------+
   |                  Apache Kafka Event Stream Bus                  |
   +-----+--------------------------+--------------------------+-----+
         |                          |                          |
         v                          v                          v
+------------------+       +------------------+       +------------------+
| Dynamic PUE Control|       |  TimescaleDB     |       | Take-or-Pay Job  |
| Microservice     |       | Aggregation Engine|      | Scheduler Engine |
+------------------+       +------------------+       +------------------+
```

### Phase 2: Algorithmic Engineering and Core Logic

We write high-performance Python/C++ control loops for automated PUE tracking and workload scheduling.

#### 2.1 Closed-Loop Dynamic PUE Optimization Control Logic

This module continuously evaluates PUE and dynamically adjusts chiller variable-frequency drive (VFD) pump speeds to prevent thermal runaways while minimizing parasitic power draw.

```Python
import time
import logging

logging.basicConfig(level=logging.INFO)

class DynamicPUEController:
    def __init__(self, setpoint_temp_c: float, kp: float, ki: float, kd: float):
        self.setpoint_temp = setpoint_temp_c
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral_error = 0.0
        self.previous_error = 0.0

    def poll_telemetry_stream(self) -> dict:
        """Simulates ingestion of high-frequency power and thermal telemetry."""
        # Returns: total_utility_kw, it_pdu_kw, fluid_return_temp_c
        return {
            "utility_kw": 14200.0,
            "it_kw": 11500.0,
            "fluid_return_temp_c": 38.5
        }

    def execute_control_step(self, dt: float) -> float:
        telemetry = self.poll_telemetry_stream()

        utility_kw = telemetry["utility_kw"]
        it_kw = telemetry["it_kw"]
        t_return = telemetry["fluid_return_temp_c"]

        # Calculate PUE and Overhead Ratio
        pue = utility_kw / it_kw if it_kw > 0 else 1.0
        overhead_ratio = pue - 1.0

        # Calculate Thermal Error Delta
        error = t_return - self.setpoint_temp
        self.integral_error += error * dt
        derivative_error = (error - self.previous_error) / dt if dt > 0 else 0.0

        # PID Actuation Signal Output (VFD Speed % adjustment)
        vfd_adjustment = (self.kp * error) + (self.ki * self.integral_error) + (self.kd * derivative_error)
        self.previous_error = error

        logging.info(f"PUE: {pue:.3f} | Overhead: {overhead_ratio:.3f} | T_Return: {t_return}°C | Actuation: {vfd_adjustment:+.2f}%")
        return vfd_adjustment

if __name__ == "__main__":
    controller = DynamicPUEController(setpoint_temp_c=32.0, kp=1.5, ki=0.1, kd=0.05)
    for _ in range(3):
        controller.execute_control_step(dt=1.0)
        time.sleep(1)
```

#### 2.2 Take-or-Pay Contractual Workload Dispatcher

This module coordinates compute job execution to maintain fuel utilization above minimum contractual thresholds under take-or-pay energy agreements.

```Python
class TakeOrPayWorkloadScheduler:
    def __init__(self, min_hourly_gas_m3: float):
        self.min_hourly_gas_m3 = min_hourly_gas_m3

    def evaluate_and_dispatch(self, current_gas_flow_m3: float, job_queue: list) -> list:
        dispatched_jobs = []
        shortfall_m3 = self.min_hourly_gas_m3 - current_gas_flow_m3

        if shortfall_m3 > 0:
            logging.warning(f"Take-or-Pay Shortfall Detected: {shortfall_m3:.2f} m3/hr below minimum!")
            # Sort jobs by power density / thermal tolerance to fill capacity
            job_queue.sort(key=lambda j: j['power_kw'], reverse=True)

            accumulated_kw = 0.0
            required_kw_boost = shortfall_m3 * 3.5  # Energy conversion constant

            for job in job_queue:
                if accumulated_kw < required_kw_boost:
                    dispatched_jobs.append(job)
                    accumulated_kw += job['power_kw']

            logging.info(f"Dispatched {len(dispatched_jobs)} batch AI jobs adding {accumulated_kw:.2f} kW compute load.")
        else:
            logging.info("Gas consumption satisfies Take-or-Pay minimum commitment.")

        return dispatched_jobs

if __name__ == "__main__":
    scheduler = TakeOrPayWorkloadScheduler(min_hourly_gas_m3=2500.0)
    queue = [
        {"job_id": "ai_train_01", "power_kw": 450.0},
        {"job_id": "ai_train_02", "power_kw": 800.0},
        {"job_id": "render_job_99", "power_kw": 200.0}
    ]
    scheduler.evaluate_and_dispatch(current_gas_flow_m3=1800.0, job_queue=queue)
```

### Phase 3: Data Schemas and Technical Integration Interfaces

Telemetry readings are stored within a distributed TimescaleDB datastore optimized for rapid time-series ingest.

#### 3.1 Industrial Telemetry Schema (PostgreSQL / TimescaleDB)

```SQL
-- Main Facility High-Frequency Telemetry Hypertable
CREATE TABLE telemetry_stream (
    timestamp           TIMESTAMPTZ NOT NULL,
    device_id           VARCHAR(64) NOT NULL,
    subsystem_type      VARCHAR(32) NOT NULL, -- 'UTILITY', 'PDU', 'CHILLER', 'IMMERSION'
    active_power_kw     DOUBLE PRECISION NULL,
    reactive_power_kvar DOUBLE PRECISION NULL,
    voltage_l1_v        DOUBLE PRECISION NULL,
    current_l1_a        DOUBLE PRECISION NULL,
    fluid_temp_c        DOUBLE PRECISION NULL,
    flow_rate_lpm       DOUBLE PRECISION NULL
);

-- Convert to Hypertable partitioned by 1-day chunks
SELECT create_hypertable('telemetry_stream', 'timestamp', chunk_time_interval => INTERVAL '1 day');

-- Continuous Aggregate View for Real-Time PUE and DCiE Computations
CREATE MATERIALIZED VIEW hourly_facility_efficiency
WITH (timescale.continuous) AS
SELECT
    time_bucket('1 hour', timestamp) AS eval_hour,
    AVG(CASE WHEN subsystem_type = 'UTILITY' THEN active_power_kw END) AS avg_gross_utility_kw,
    AVG(CASE WHEN subsystem_type = 'PDU' THEN active_power_kw END) AS avg_it_compute_kw,

    -- Calculated PUE
    AVG(CASE WHEN subsystem_type = 'UTILITY' THEN active_power_kw END) /
    NULLIF(AVG(CASE WHEN subsystem_type = 'PDU' THEN active_power_kw END), 0) AS real_time_pue,

    -- Calculated DCiE (%)
    (NULLIF(AVG(CASE WHEN subsystem_type = 'PDU' THEN active_power_kw END), 0) /
    AVG(CASE WHEN subsystem_type = 'UTILITY' THEN active_power_kw END)) * 100.0 AS real_time_dcie_pct
FROM telemetry_stream
GROUP BY eval_hour;
```

### Phase 4: Quality Assurance, Verification, and Fault Injection

Software engines are subjected to rigorous quality assurance before deployment to production environments:

1. **Hardware-in-the-Loop (HIL) Emulation**: Microservices connect to simulated Modbus/SNMP software stubs mimicking gas engine trip events, rapid ambient heat surges ($+10^\circ\text{C}$ step jump), and PDU meter disconnects.

2. **Chaos Mesh Network Fault Injection**: Packet loss rates (up to 30%) and latency delays (up to 2,000 ms) are injected into the ingestion pipeline. Verification criteria demand zero data dropouts in TimescaleDB, supported by local edge buffer retries.

3. **PUE Calculation Boundary Verification**: Continuous unit tests validate edge cases—specifically verifying that under zero-load conditions ($E_{\text{IT}} = 0$), the PUE engine handles division by zero gracefully without throwing unhandled control exceptions.

### Phase 5: Production Deployment and Model Maintenance

- **Edge/Cloud Hybrid Deployment**: Physical control loops run locally on high-availability edge servers within the facility to maintain low execution latencies (<50 ms). Aggregated time-series data is synchronized to the central cloud dashboard over encrypted TLS 1.3 channels.

- **Continuous Model Retraining**: Machine learning heat-rejection models are automatically retrained monthly using updated empirical operational data, capturing physical degradation in heat exchangers or cooling pumps. Updated binary weights are deployed to edge containers via continuous integration and continuous deployment (CI/CD) pipelines.

## 7. Cross-Disciplinary Integration Interface Matrix

Computer Scientist #1 serves as a central integration link, exchanging critical datasets with all other project engineering roles:

```
+-----------------------------------------------------------------------------------+
|                        CROSS-DISCIPLINARY DATA INTERACTION MATRIX                 |
+-----------------------------------------------------------------------------------+
| CS #1 Outbound Outputs                                                            |
|   ├──> Electrical Eng.  : Hourly Load Profile (MW) -> Sizes Generators/UPS        |
|   ├──> Mechanical Eng.  : Rack Densities & Heat Output -> Sizes Cooling Systems   |
|   └──> Comp. Sci. #2    : PUE Baselines & Telemetry -> Drives Financial OPEX    |
|                                                                                   |
| CS #1 Inbound Inputs                                                              |
|   ├──< Petroleum Eng.   : Delivered Fuel Cost ($/MMBtu) & Supply Guarantees     |
|   ├──< Electrical Eng.  : Electrical CAPEX, Parasitic Losses & Switchgear Specs   |
|   └──< Mechanical Eng.  : Chiller Efficiency Curves & Dynamic Parasitic Load    |
+-----------------------------------------------------------------------------------+
```

| **Source Role**           | **Target Role**           | **Shared Technical Variable / Data Payload**                              | **Engineering Impact & Dependencies**                                                             |
| ------------------------- | ------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Computer Scientist #1** | **Electrical Engineer**   | 24-Hour Hourly Load Demand Curve ($E_{\text{IT}}$ in MW)                  | Establishes prime mover generator capacity ratings (gas engines vs. CCGT) and UPS battery sizing. |
| **Computer Scientist #1** | **Mechanical Engineer**   | Heat Dissipation Density ($Q_{\text{thermal}}$ per rack zone)             | Determines direct-to-chip vs. liquid immersion cooling flow rates ($\dot{m}$) and pipe layout.    |
| **Computer Scientist #1** | **Computer Scientist #2** | Real-Time $PUE$, $DCiE$, and Annual kWh Consumption                       | Inputs baseline operating metrics into the master financial model (LCOE, NPV, IRR calculation).   |
| **Petroleum Engineer**    | **Computer Scientist #1** | Delivered Fuel Cost ($/MMBtu) & Supply Availability                       | Feeds contractual fuel pricing into the take-or-pay automated job dispatch engine.                |
| **Mechanical Engineer**   | **Computer Scientist #1** | Chiller & Pump COP Curves ($E_{\text{Cooling}}$ vs. $T_{\text{Ambient}}$) | Provides physical efficiency bounds for dynamic closed-loop software control algorithms.          |

## 8. Summary Checklist for Team Coordination Meeting

During the upcoming team synchronization meeting, **Computer Scientist #1** will confirm the following baseline parameters:

- [x] **Target IT Capacity Locked**: $12.0\text{ MW}$ net compute load within a $15.0\text{ MW}$ gross generator cap ($PUE = 1.25$).

- [x] **Rack Density Distribution**: 250 racks @ 20 kW/rack (Cloud), 80 racks @ 50 kW/rack (HPC), 30 racks @ 100 kW/rack (AI Immersion).

- [x] **Telemetry Architecture Finalized**: Apache Kafka + TimescaleDB edge microservices handling Modbus/BACnet/SNMP ingestion.

- [x] **Algorithmic Modules Prepared**: Automated PID thermal cooling control + Take-or-pay fuel contract workload dispatcher.

