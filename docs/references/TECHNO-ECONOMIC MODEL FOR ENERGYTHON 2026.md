### What is Techno-Economic

A **techno-economic model** is a comprehensive analytical framework that integrates **technical engineering data** with **financial economic analysis** to determine the feasibility and viability of a project. 

For the specific challenge of designing a power solution for a **10–20 MW data center**, "techno-economic" means the participants must simultaneously solve two interconnected problems:

### 1. The Technical Dimension ("Techno")

Participants must define the physical engineering architecture required to reliably power the data center. This includes:

- **Power Generation Design**: Sizing the natural gas-fired power plant (e.g., turbines, generators) to meet the 10–20 MW load.
    
- **Efficiency & Performance**: Calculating heat rates, fuel consumption, and energy conversion efficiency.
    
- **Reliability & Redundancy**: Ensuring the system meets data center uptime standards (e.g., Tier III or IV) through backup systems and maintenance schedules.
    
- **Supply Chain Logistics**: Planning the fuel supply infrastructure (pipelines, storage) needed to sustain continuous operation. 
    

### 2. The Economic Dimension ("Economic")

Participants must translate the technical design into financial metrics to prove the project is a sound investment. This includes:

- **Capital Expenditure (CAPEX)**: Estimating the upfront costs for equipment, construction, and land.
    
- **Operational Expenditure (OPEX)**: Projecting ongoing costs such as natural gas fuel prices, maintenance, labor, and insurance.
    
- **Financial Viability**: Calculating key metrics like the **Levelized Cost of Energy (LCOE)**, Net Present Value (NPV), Internal Rate of Return (IRR), and payback period. 
    
- **Revenue Modeling**: Determining the price per kilowatt-hour (kWh) or capacity charge needed to recover costs and generate profit.
    

### The Integration

The core of the challenge is the **interdependency** of these factors. A technical decision (e.g., choosing a more efficient but expensive turbine) directly alters the economic outcome (higher CAPEX but lower fuel OPEX). The model must optimize this balance to present a solution that is not only **engineerably sound** but also **commercially competitive** in a "Shark Tank" style pitch.

## DATA CENTER ARCHITECTURE AND LOAD PROFILING

**Data Center Architecture and Load Profiling** for the SPE Energython, the role is to translate physical power constraints into computational requirements and efficiency metrics. Here is the breakdown of your three specific research areas:

### 1. IT Architecture Sizing

This involves determining the optimal hardware configuration to maximize computational output within the fixed energy envelope provided by the techno-economic model (10–20 MW).

- **Compute Density & Rack Layout**: You must calculate the number of racks and servers that fit the power budget. This requires selecting hardware (CPUs, GPUs, TPUs) based on **Performance-per-Watt** rather than just raw performance. For a 20 MW cap, you might prioritize high-density AI clusters over general-purpose cloud servers.
    
- **Power Distribution Unit (PDU) Planning**: Define the electrical hierarchy from the substation to the rack. You need to size PDUs and busways to handle peak loads without tripping, ensuring the **IT load** matches the **available facility power**.
    
- **Scalability Modeling**: Create a modular architecture (e.g., pod-based design) that allows the data center to scale from 10 MW to 20 MW as demand grows, without requiring a complete redesign of the power infrastructure.
### Sources
[Data Center Power](https://dgtlinfra.com/data-center-power/)

[Best Practices for data center sizing](https://www.profileits.com/best-practices-for-data-center-area-sizing-per-rack-based-on-power-density/)

[Data Center Power Planning](https://datacenterss.com/data-center-power-planning-calculation-guide/)

[data center IT architecture sizing power density](https://search.brave.com/search?q=data%20center%20IT%20architecture%20sizing%20power%20density)

### 2. Load Demand Profiling

This requires analyzing _how_ and _when_ the IT equipment consumes power to ensure the generation source (likely natural gas turbines in this context) can handle dynamic shifts without instability.

- **Workload Characterization**: Distinguish between **baseline load** (idle systems, networking, cooling fans) and **dynamic load** (compute spikes). For example, AI training jobs create sustained high loads, while web serving creates bursty, unpredictable spikes.
    
- **Temporal Analysis**: Map load variations over time (hourly, daily, seasonal). You must identify the **Peak-to-Average Ratio (PAR)**. A high PAR requires expensive over-provisioning of generators, whereas a flat profile allows for higher efficiency.
    
- **Power Capping & Throttling**: Develop algorithms to dynamically throttle non-critical workloads when the total facility load approaches the 20 MW limit, ensuring the power plant never trips due to sudden demand surges.

### Sources
[Watch Video](https://www.youtube.com/watch?v=F-xDuOy-6-8)

[Watch Video](https://www.youtube.com/watch?v=cGz3MdKrhx4)

[Watch Video](https://www.youtube.com/watch?v=fTsZwKcfxYc)

[Watch Video](https://www.youtube.com/watch?v=qjSse9T_1yY)

[Watch Video](https://www.youtube.com/watch?v=GJiBqvUl5rU)

[data center load profiling and demand response](https://search.brave.com/videos?q=data%20center%20load%20profiling%20and%20demand%20response)

### 3. Target PUE Benchmarking

**Power Usage Effectiveness (PUE)** is the primary metric for efficiency, defined as $\text{PUE} = \frac{\text{Total Facility Energy}}{\text{IT Equipment Energy}}$. Your goal is to minimize the "overhead" energy (cooling, lighting, conversion losses).

- **Cooling Architecture Selection**: As a computer scientist, you influence PUE by designing software-defined cooling strategies. This includes implementing **liquid cooling** (direct-to-chip or immersion) which drastically reduces fan energy and allows higher operating temperatures compared to traditional air cooling.
    
- **Thermal Modeling & CFD**: Use Computational Fluid Dynamics (CFD) simulations to optimize airflow, eliminating hot spots and reducing the need for aggressive air conditioning. The target for a modern, efficient data center is a PUE of **1.1 to 1.2**.
    
- **Benchmarking Strategy**: Compare your design against industry standards (e.g., Uptime Institute, ASHRAE guidelines). You must justify your target PUE in the economic model: a lower PUE reduces fuel costs (OPEX) but may increase initial infrastructure costs (CAPEX).
    
**Power usage effectivenessindicator:** ratio that describes how efficiently a computer data center uses energy; specifically, how much energy is used by the computing equipment (in contrast to cooling and other overhead)

[Wikipedia](https://en.wikipedia.org/wiki/Power_usage_effectiveness)

### Integration for the Energython

The output feeds directly into the techno-economic model:

1. **Sizing** determines the maximum revenue-generating capacity (IT Load).
    
2. **Profiling** determines the stability requirements and fuel consumption patterns.
    
3. **PUE** determines the non-revenue energy waste, directly impacting the Levelized Cost of Energy (LCOE).
    
### Sources
[PUE WUE AI Data Centers](https://clearcomfort.com/pue-wue-ai-data-centers/)

[What are the power requirements for AI data centers](https://www.hanwhadatacenters.com/blog/what-are-the-power-requirements-for-ai-data-centers/)

[Data Center efficiency strategy](https://introl.com/blog/pue-109-google-data-center-efficiency-strategies)

### Overview

The primary objective is to define the **IT Load Profile** and **Efficiency Baseline** that will drive the techno-economic model. The engineering team (power generation) depends on your data to size turbines and fuel storage, while the finance team needs your efficiency metrics to calculate the Levelized Cost of Energy (LCOE).

Your specific deliverable is a **Data Center Load & Efficiency Report** containing three critical components:

#### 1. Realistic Load Demand Curves

You must generate time-series data (typically 8,760 hours for one year) representing the power consumption of the IT equipment. This is not a flat line; it must reflect the distinct behaviors of AI and Cloud workloads.

- **Idle vs. Peak Baseline**: Define the "baseload" power (fans, networking, idle servers) versus the "compute" power. Modern GPUs often have an idle-to-peak ratio of **30% to 40%**, meaning even at "idle," a rack draws significant power compared to legacy CPUs.
    
- **Diurnal Fluctuations**:
    
    - **Cloud Workloads**: Typically follow a human-centric diurnal pattern (peaking during business hours, 9 AM–6 PM local time, with dips at night).
        
    - **AI Workloads**: Unlike cloud, AI training jobs are **sustained and flat**.  Once a training run starts, it often runs at 95–100% load for days or weeks without dipping. Inference workloads may follow user traffic patterns but are increasingly 24/7 global services.
        
- **The Deliverable**: A dataset or graph showing **Total IT Power (kW)** vs. **Time (Hours)**.  Should provide scenarios:
    
    - _Scenario A (Cloud Heavy)_: High variance, distinct day/night cycles.
        
    - _Scenario B (AI Heavy)_: High baseload, sustained peaks, minimal diurnal drop.
        
    - _Scenario C (Mixed)_: A realistic hybrid curve where base AI training provides a floor, and cloud/inference adds diurnal spikes. 
        
### Sources
[Watch Video](https://www.youtube.com/watch?v=M9eozcgX-Fs)

[Watch Video](https://www.youtube.com/watch?v=ffXVCC1ZmAg)

[Watch Video](https://www.youtube.com/watch?v=6HjrkSoeN2I)

[Watch Video](https://www.youtube.com/watch?v=ycLJuNu2DKs)

[Watch Video](https://www.youtube.com/watch?v=l1_6gGAPN10)

[AI vs Cloud data center load profiles explained](https://search.brave.com/videos?q=AI%20vs%20Cloud%20data%20center%20load%20profiles%20explained)

#### 2. Target PUE Benchmarking for Warm/Tropical Climates

Since the Energython targets regions like Africa (as noted in the AMTS student chapter context), you cannot use standard "cool climate" PUE values (e.g., 1.15). You must establish a **climate-adjusted baseline**.

- **Realistic Values**: In warm or tropical climates (ambient temps >30°C/86°F), traditional air-side economizers are ineffective for much of the year.
    
    - **Standard Air-Cooled**: Expect a realistic PUE of **1.45 – 1.60**. The cooling chillers must work harder against the high ambient wet-bulb temperatures.
        
    - **Advanced/Liquid-Cooled**: If your architecture proposes direct-to-chip or immersion cooling, you can target **1.20 – 1.30**. Liquid cooling is less sensitive to ambient air temperature, making it superior for tropical deployments.
        
- **The Deliverable**: A justification table selecting a **Target PUE** (e.g., 1.35) based on your proposed cooling architecture. You must explicitly state: _"Given a tropical ambient design temperature of 35°C, a traditional air-cooled facility would achieve 1.55 PUE. By utilizing [Your Architecture, e.g., rear-door heat exchangers], we target a PUE of 1.35."_ 
    

[What is Power Usage Effectiveness](https://cove.inc/blog/what-is-power-usage-effectiveness-pue-data-center-efficiency/)

[What is PUE in data centers](https://www.asperitas.com/post/what-is-pue-in-a-datacentre)

[Understanding measuring and improving PUE](https://www.score-grp.com/en/post/data-center-pue-in-2026-understanding-measuring-and-improving-power-usage-effectiveness)

[data center PUE tropical climate benchmarks 2026](https://search.brave.com/search?q=data%20center%20PUE%20tropical%20climate%20benchmarks%202026)

#### 3. IT Architecture Sizing Logic

You must translate the 10–20 MW _facility_ limit into _IT_ capacity.

- **The Calculation**: $\text{IT Load} = \frac{\text{Total Facility Power}}{\text{PUE}}$.
    
    - If the power plant provides **20 MW** and your **PUE is 1.4**, your maximum **IT Load is ~14.3 MW**.
        
    - If you optimize to **PUE 1.2**, your **IT Load increases to ~16.6 MW** (more revenue-generating compute). 
        
- **The Deliverable**: A specification sheet detailing:
    
    - **Total IT Capacity (MW)**: The net power available for servers.
        
    - **Rack Density (kW/rack)**: Are you designing for high-density AI racks (40–100 kW) or standard cloud racks (10–20 kW)?
        
    - **Server Count Estimate**: Based on average server wattage (e.g., 1 kW per GPU server).
        

### Summary of Expected Deliverables

| Component         | Format                  | Key Data Points to Include                                                                                     |
| ----------------- | ----------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Load Profiles** | CSV / Time-Series Graph | Hourly kW demand for 1 year; Distinct curves for Idle, Peak, AI (sustained), and Cloud (diurnal).              |
| **PUE Benchmark** | Technical Memo          | Target PUE value (e.g., 1.35); Justification based on tropical climate constraints; Cooling technology choice. |
| **IT Sizing**     | Specification Sheet     | Max IT Load (MW); Rack count; Density per rack; Breakdown of Compute vs. Storage power.                        |

Power usage effectivenessindicator: ratio that describes how efficiently a computer data center uses energy; specifically, how much energy is used by the computing equipment (in contrast to cooling and other overhead)

[Wikipedia](https://en.wikipedia.org/wiki/Power_usage_effectiveness)

Your work provides the "Demand" side of the equation. If your load profiles are too optimistic (flat lines) or your PUE is too low (ignoring the heat), the techno-economic model will underestimate fuel costs and overestimate profitability, causing the team's "Shark Tank" pitch to fail on technical feasibility.

## TECHNICAL TERMS DEFINITIONS
### **Architecture & Sizing**

- **Data Center Architecture**: The holistic design of the facility, encompassing the physical layout, power distribution, cooling systems, and IT hardware arrangement to maximize efficiency and reliability.
    
- **IT Infrastructure Sizing**: The calculation of the total number of servers, storage units, and network switches that can be supported within a specific power budget (e.g., fitting enough GPUs to utilize 15 MW of IT load).
    
- **Server Density / Power Rack Density**: The amount of power consumed by a single server rack, measured in **kW/rack**.
    
    - _Context_: Traditional cloud racks average **10–20 kW**, while modern AI GPU racks often exceed **40–100 kW**, requiring liquid cooling. 
        
- **Total Compute Capacity**: The aggregate processing power available, often expressed as the total **IT Load (MW)** or in FLOPS (floating-point operations per second), representing the revenue-generating potential of the facility.
    

### **Load Profiling & Curves**

- **Load Demand Profiling**: The analysis of how power consumption fluctuates over time to predict energy needs and prevent grid instability. 
    
- **Realistic Load Curves**: Graphs plotting power usage (kW) against time (hours), avoiding flat lines to show real-world variability.
    
- **Idle Power**: The baseline energy consumed by servers when not actively processing heavy tasks (fans, memory, idle CPUs).
    
    - _Note_: Modern GPU servers still draw **30–40%** of peak power even at idle. 
        
- **Peak Load Demand**: The maximum power draw during intense computation; infrastructure must be sized to handle this without tripping. 
    
- **Diurnal Fluctuations**: Daily cycles in power usage.
    
    - _Cloud Workloads_: Typically peak during business hours (9 AM–6 PM) and dip at night.
        
    - _AI Workloads_: Training jobs often create **sustained, flat peaks** for days, while inference follows user traffic patterns. 
        
- **AI/Cloud Workloads**:
    
    - _Cloud_: Bursty, latency-sensitive, CPU-heavy, variable demand.
        
    - _AI_: Sustained, high-density, GPU-heavy, often running at 90–100% utilization for long durations. 
        

### **Efficiency & Benchmarking**

- **PUE (Power Usage Effectiveness)**: The ratio of **Total Facility Energy** divided by **IT Equipment Energy**.
    
    - _Formula_: $\text{PUE} = \frac{\text{IT Load} + \text{Cooling} + \text{Lighting} + \text{Losses}}{\text{IT Load}}$.
        
    - _Goal_: Closer to **1.0** is better (1.0 means all power goes to IT).
        
- **PUE Benchmarking**: Comparing your facility's PUE against industry standards or similar climates to validate efficiency claims. 
    
- **Real-time Data Center PUE Values**: Dynamic PUE measurements that fluctuate hourly based on external weather and IT load, rather than a single static annual number. 
    
- **Realistic Base Cases**: Conservative starting assumptions for your model.
    
    - _Tropical Context_: In warm climates, a realistic base case for air-cooled facilities is **PUE 1.45–1.60**. Advanced liquid-cooled designs might target **1.20–1.30**. Using a temperate climate value (e.g., 1.15) in a tropical model would be unrealistic.
        

[Data Center Grossary](https://stlpartners.com/articles/data-centres/data-centres-glossary/)

[Data Center Grossary](https://pducables.com/resources/glossary-of-data-center-terms)

[Data Center Grossary](https://www.dvlnet.com/resources/glossarycategory)

[Traver Smith Knowledge data center terms](https://www.traverssmith.com/knowledge/knowledge-container/an-a-z-guide-to-data-centre-terminology/)


