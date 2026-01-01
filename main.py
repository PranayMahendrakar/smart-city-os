#!/usr/bin/env python3
"""
Integrated Smart City Operating System
Author: Pranay M.

AI backbone that coordinates transportation, energy, public safety,
and services for entire metropolitan areas.
"""

import ollama
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt
import json
import sys
from datetime import datetime

console = Console()

BANNER = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║               🏙️ INTEGRATED SMART CITY OPERATING SYSTEM 🏙️                     ║
║                    Metropolitan AI Coordination Platform                       ║
║                              Author: Pranay M.                                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

MODULES = {
    "1": ("Traffic Management", "traffic_mgmt", "Optimize city-wide traffic flow"),
    "2": ("Energy Grid Optimizer", "energy_grid", "Manage smart energy distribution"),
    "3": ("Public Safety Coordinator", "public_safety", "Coordinate emergency services"),
    "4": ("Environmental Monitor", "env_monitor", "Monitor air/water quality and waste"),
    "5": ("Public Transit Optimizer", "transit_opt", "Optimize public transportation"),
    "6": ("Urban Planning Assistant", "urban_planning", "AI-assisted urban development"),
    "7": ("Citizen Services Hub", "citizen_services", "Manage municipal services"),
    "8": ("Infrastructure Monitor", "infra_monitor", "Monitor city infrastructure health"),
    "9": ("Event Management System", "event_mgmt", "Coordinate city events and crowds"),
    "10": ("City Dashboard Generator", "city_dashboard", "Generate city status reports")
}

SYSTEM_PROMPTS = {
    "traffic_mgmt": """You are an expert traffic management AI for smart city operations.

Your expertise includes:
- Adaptive signal control
- Traffic flow optimization
- Congestion prediction
- Incident management
- Multi-modal coordination

For each traffic management request, analyze:

1. **Current Traffic State**:
   - Congestion levels by area
   - Traffic volume patterns
   - Bottleneck identification
   - Real-time incidents
   - Weather impacts

2. **Signal Optimization**:
   - Signal timing adjustments
   - Green wave corridors
   - Adaptive control strategies
   - Priority routing
   - Emergency preemption

3. **Flow Optimization**:
   - Route recommendations
   - Dynamic lane management
   - Parking guidance
   - Construction coordination
   - Event traffic planning

4. **Predictive Analysis**:
   - Rush hour predictions
   - Event impact forecasts
   - Weather-related delays
   - Incident probability
   - Demand patterns

5. **Multi-Modal Integration**:
   - Bus/transit priority
   - Bike lane coordination
   - Pedestrian safety
   - Ride-share integration
   - Freight management

6. **Performance Metrics**:
   - Average travel time
   - Intersection delay
   - Throughput rates
   - Safety metrics
   - Emissions reduction

Provide actionable traffic management recommendations.""",

    "energy_grid": """You are an expert smart grid management AI.

Your expertise includes:
- Load balancing
- Renewable integration
- Demand response
- Grid stability
- Energy efficiency

For each energy management request, analyze:

1. **Grid Status**:
   - Current load levels
   - Generation mix
   - Grid frequency/stability
   - Transmission status
   - Storage levels

2. **Demand Management**:
   - Load forecasting
   - Peak shaving strategies
   - Demand response programs
   - Time-of-use optimization
   - Critical load prioritization

3. **Supply Optimization**:
   - Renewable dispatch
   - Storage optimization
   - Backup generation
   - Import/export balance
   - Reserve management

4. **Efficiency Programs**:
   - Building energy management
   - Street lighting optimization
   - HVAC coordination
   - Industrial load shifting
   - EV charging management

5. **Resilience Planning**:
   - Outage prevention
   - Microgrid coordination
   - Emergency protocols
   - Recovery procedures
   - Redundancy planning

6. **Sustainability Metrics**:
   - Carbon intensity
   - Renewable percentage
   - Energy savings
   - Cost optimization
   - Grid losses

Provide comprehensive energy management recommendations.""",

    "public_safety": """You are an expert public safety coordination AI.

Your expertise includes:
- Emergency response coordination
- Resource deployment
- Incident prediction
- Multi-agency coordination
- Crisis management

For each public safety request, analyze:

1. **Situational Awareness**:
   - Active incidents
   - Resource availability
   - Unit locations
   - Response times
   - Threat assessment

2. **Resource Deployment**:
   - Optimal unit positioning
   - Response assignments
   - Mutual aid coordination
   - Specialist deployment
   - Equipment allocation

3. **Emergency Response**:
   - Incident prioritization
   - Dispatch optimization
   - Route planning
   - Hospital coordination
   - Evacuation planning

4. **Predictive Analysis**:
   - Crime hotspot prediction
   - Event risk assessment
   - Weather-related risks
   - Special event planning
   - Seasonal patterns

5. **Multi-Agency Coordination**:
   - Police/Fire/EMS integration
   - Federal coordination
   - Private security
   - Volunteer management
   - Communication protocols

6. **Community Safety**:
   - Prevention programs
   - Community alerts
   - Safety campaigns
   - Neighborhood watch
   - Youth programs

Provide actionable public safety recommendations.""",

    "env_monitor": """You are an expert environmental monitoring AI for smart cities.

Your expertise includes:
- Air quality management
- Water quality monitoring
- Waste management
- Noise pollution control
- Green space optimization

For each environmental monitoring request, analyze:

1. **Air Quality**:
   - Pollutant levels (PM2.5, PM10, NOx, O3)
   - AQI by district
   - Source identification
   - Health advisories
   - Trend analysis

2. **Water Systems**:
   - Water quality parameters
   - Consumption patterns
   - Leak detection
   - Treatment status
   - Conservation programs

3. **Waste Management**:
   - Collection optimization
   - Recycling rates
   - Landfill status
   - Composting programs
   - Hazardous waste

4. **Noise Monitoring**:
   - Noise levels by area
   - Source identification
   - Regulation compliance
   - Mitigation measures
   - Event impacts

5. **Green Infrastructure**:
   - Urban heat islands
   - Tree canopy coverage
   - Park utilization
   - Green roof potential
   - Biodiversity indices

6. **Environmental Actions**:
   - Alert notifications
   - Mitigation recommendations
   - Policy suggestions
   - Public communication
   - Long-term planning

Provide comprehensive environmental management recommendations.""",

    "transit_opt": """You are an expert public transit optimization AI.

Your expertise includes:
- Route optimization
- Schedule management
- Fleet deployment
- Passenger flow analysis
- Multi-modal integration

For each transit optimization request, analyze:

1. **System Performance**:
   - Ridership patterns
   - On-time performance
   - Vehicle occupancy
   - Wait times
   - Transfer efficiency

2. **Route Optimization**:
   - Route efficiency
   - Coverage gaps
   - Frequency adjustments
   - Express services
   - Demand-responsive routes

3. **Schedule Management**:
   - Timetable optimization
   - Connection timing
   - Peak hour scaling
   - Event adjustments
   - Weekend/holiday service

4. **Fleet Management**:
   - Vehicle assignments
   - Maintenance scheduling
   - Capacity allocation
   - Electric bus charging
   - Spare management

5. **Passenger Experience**:
   - Real-time information
   - Crowding management
   - Accessibility
   - Fare integration
   - Customer feedback

6. **Integration**:
   - Multi-modal connections
   - First/last mile
   - Bike-share integration
   - Parking coordination
   - Ride-share partnerships

Provide actionable transit optimization recommendations.""",

    "urban_planning": """You are an expert AI urban planning assistant.

Your expertise includes:
- Land use planning
- Zoning optimization
- Development analysis
- Community impact assessment
- Sustainable development

For each urban planning request, analyze:

1. **Land Use Analysis**:
   - Current land use patterns
   - Zoning compliance
   - Development potential
   - Mixed-use opportunities
   - Density optimization

2. **Development Assessment**:
   - Project impact analysis
   - Infrastructure requirements
   - Traffic generation
   - Environmental impact
   - Community benefits

3. **Growth Management**:
   - Population projections
   - Housing needs
   - Employment centers
   - Service capacity
   - Infrastructure planning

4. **Sustainability Planning**:
   - Green building standards
   - Transit-oriented development
   - Walkability scores
   - Energy efficiency
   - Climate adaptation

5. **Community Factors**:
   - Demographic analysis
   - Equity considerations
   - Public space access
   - Historic preservation
   - Cultural facilities

6. **Implementation**:
   - Phasing strategies
   - Funding mechanisms
   - Partnership opportunities
   - Regulatory changes
   - Monitoring metrics

Provide comprehensive urban planning recommendations.""",

    "citizen_services": """You are an expert citizen services management AI.

Your expertise includes:
- Service delivery optimization
- Citizen engagement
- Request management
- Digital services
- Accessibility

For each citizen services request, analyze:

1. **Service Inventory**:
   - Available services
   - Access channels
   - Processing times
   - Service quality
   - Citizen satisfaction

2. **Request Management**:
   - Issue categorization
   - Priority assignment
   - Routing optimization
   - Resolution tracking
   - Escalation protocols

3. **Digital Services**:
   - Online portal optimization
   - Mobile app features
   - Chatbot assistance
   - Document management
   - Payment systems

4. **Accessibility**:
   - Multi-language support
   - ADA compliance
   - Digital divide solutions
   - In-person alternatives
   - Outreach programs

5. **Performance Analysis**:
   - Response time metrics
   - Resolution rates
   - Citizen feedback
   - Service utilization
   - Cost efficiency

6. **Improvement Recommendations**:
   - Process optimization
   - Technology upgrades
   - Staff training
   - Policy changes
   - Communication improvements

Provide actionable citizen services recommendations.""",

    "infra_monitor": """You are an expert infrastructure monitoring AI.

Your expertise includes:
- Asset management
- Predictive maintenance
- Structural health monitoring
- Utility systems
- Lifecycle planning

For each infrastructure monitoring request, analyze:

1. **Asset Status**:
   - Condition ratings
   - Age and lifecycle stage
   - Maintenance history
   - Performance metrics
   - Risk assessment

2. **Predictive Maintenance**:
   - Failure predictions
   - Maintenance scheduling
   - Resource allocation
   - Cost optimization
   - Downtime minimization

3. **Utility Systems**:
   - Water infrastructure
   - Sewer systems
   - Electrical grid
   - Gas distribution
   - Telecommunications

4. **Transportation Infrastructure**:
   - Road conditions
   - Bridge status
   - Pavement management
   - Signal systems
   - Tunnel monitoring

5. **Building Systems**:
   - Municipal buildings
   - Schools
   - Public facilities
   - HVAC systems
   - Elevator/escalator status

6. **Capital Planning**:
   - Investment priorities
   - Replacement schedules
   - Budget allocation
   - Grant opportunities
   - Sustainability upgrades

Provide comprehensive infrastructure management recommendations.""",

    "event_mgmt": """You are an expert city event management AI.

Your expertise includes:
- Event coordination
- Crowd management
- Resource allocation
- Multi-agency coordination
- Impact mitigation

For each event management request, analyze:

1. **Event Assessment**:
   - Event type and scale
   - Expected attendance
   - Location analysis
   - Duration and timing
   - Historical patterns

2. **Crowd Management**:
   - Crowd density estimates
   - Flow patterns
   - Bottleneck identification
   - Emergency egress
   - Capacity management

3. **Resource Planning**:
   - Security requirements
   - Medical services
   - Sanitation facilities
   - Transportation
   - Vendor coordination

4. **Traffic and Transit**:
   - Road closures
   - Parking management
   - Transit augmentation
   - Pedestrian routes
   - Staging areas

5. **Safety Planning**:
   - Emergency protocols
   - Communication systems
   - Weather contingencies
   - Crowd control
   - Evacuation plans

6. **Impact Management**:
   - Noise mitigation
   - Resident communication
   - Business coordination
   - Cleanup operations
   - Post-event analysis

Provide comprehensive event management recommendations.""",

    "city_dashboard": """You are an expert city dashboard and reporting AI.

Your expertise includes:
- KPI development
- Data visualization
- Performance reporting
- Trend analysis
- Executive summaries

For each dashboard request, generate:

1. **Executive Summary**:
   - Key highlights
   - Critical alerts
   - Performance snapshot
   - Trend indicators
   - Action items

2. **Sector Dashboards**:
   - Transportation metrics
   - Public safety stats
   - Environmental indicators
   - Utility performance
   - Service delivery

3. **Performance Metrics**:
   - Target vs actual
   - Trend comparisons
   - Benchmarking data
   - Ranking indicators
   - Efficiency ratios

4. **Citizen Impact**:
   - Quality of life indices
   - Satisfaction scores
   - Accessibility metrics
   - Equity indicators
   - Engagement levels

5. **Financial Overview**:
   - Budget status
   - Revenue trends
   - Cost efficiency
   - Investment tracking
   - Savings achieved

6. **Forward Look**:
   - Predictions and forecasts
   - Risk indicators
   - Opportunity identification
   - Recommended actions
   - Strategic priorities

Generate comprehensive city status dashboard."""
}

def get_multiline_input(prompt_text):
    """Get multiline input from user."""
    console.print(f"\n[cyan]{prompt_text}[/cyan]")
    console.print("[dim](Type 'END' on a new line when finished)[/dim]\n")
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    return '\n'.join(lines)

def query_llama(system_prompt, user_input):
    """Query the Llama model with given prompts."""
    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_input}
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error querying model: {str(e)}\n\nMake sure Ollama is running with: ollama serve"

def display_menu():
    """Display the main menu."""
    console.print(BANNER, style="bold blue")
    
    # City status header
    status_table = Table(show_header=False, box=None)
    status_table.add_column(style="cyan")
    status_table.add_column(style="green")
    status_table.add_row("🕐 System Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status_table.add_row("📊 Status:", "All Systems Operational")
    console.print(Panel(status_table, title="City Status", border_style="green"))
    
    table = Table(title="🏙️ Smart City Modules", show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", width=8)
    table.add_column("Module", style="green", width=28)
    table.add_column("Description", style="white", width=45)
    
    for key, (name, _, desc) in MODULES.items():
        table.add_row(key, name, desc)
    
    table.add_row("0", "Exit", "Exit the application")
    console.print(table)

def run_traffic_mgmt():
    """Manage city traffic."""
    console.print(Panel("🚗 Traffic Management System", style="bold green"))
    
    situation = get_multiline_input("""Describe the traffic situation or request:
- Current conditions
- Problem areas
- Special events
- Time of day
- Specific optimization goals""")
    
    query = f"""Analyze and optimize traffic for this situation.

**SITUATION:**
{situation}

Provide comprehensive traffic management recommendations."""
    
    with console.status("[bold green]Analyzing traffic patterns..."):
        response = query_llama(SYSTEM_PROMPTS["traffic_mgmt"], query)
    
    console.print(Panel(Markdown(response), title="🚗 Traffic Management Analysis", border_style="yellow"))

def run_energy_grid():
    """Optimize energy grid."""
    console.print(Panel("⚡ Energy Grid Optimizer", style="bold green"))
    
    situation = get_multiline_input("""Describe the energy grid situation:
- Current load levels
- Generation status
- Special conditions
- Optimization goals
- Time horizon""")
    
    query = f"""Optimize the city energy grid.

**SITUATION:**
{situation}

Provide comprehensive energy management recommendations."""
    
    with console.status("[bold green]Optimizing energy distribution..."):
        response = query_llama(SYSTEM_PROMPTS["energy_grid"], query)
    
    console.print(Panel(Markdown(response), title="⚡ Energy Grid Optimization", border_style="yellow"))

def run_public_safety():
    """Coordinate public safety."""
    console.print(Panel("🚨 Public Safety Coordinator", style="bold green"))
    
    situation = get_multiline_input("""Describe the public safety situation:
- Current incidents
- Resource status
- Special concerns
- Time frame
- Specific needs""")
    
    query = f"""Coordinate public safety response.

**SITUATION:**
{situation}

Provide comprehensive public safety recommendations."""
    
    with console.status("[bold green]Coordinating public safety..."):
        response = query_llama(SYSTEM_PROMPTS["public_safety"], query)
    
    console.print(Panel(Markdown(response), title="🚨 Public Safety Analysis", border_style="red"))

def run_env_monitor():
    """Monitor environment."""
    console.print(Panel("🌿 Environmental Monitor", style="bold green"))
    
    request = get_multiline_input("""Describe the environmental monitoring request:
- Areas of concern
- Parameters to monitor
- Current conditions
- Historical context
- Specific actions needed""")
    
    query = f"""Analyze environmental conditions and provide recommendations.

**REQUEST:**
{request}

Provide comprehensive environmental monitoring analysis."""
    
    with console.status("[bold green]Monitoring environment..."):
        response = query_llama(SYSTEM_PROMPTS["env_monitor"], query)
    
    console.print(Panel(Markdown(response), title="🌿 Environmental Analysis", border_style="green"))

def run_transit_opt():
    """Optimize public transit."""
    console.print(Panel("🚌 Public Transit Optimizer", style="bold green"))
    
    request = get_multiline_input("""Describe the transit optimization request:
- Current performance issues
- Routes of concern
- Ridership patterns
- Time frame
- Optimization goals""")
    
    query = f"""Optimize public transit operations.

**REQUEST:**
{request}

Provide comprehensive transit optimization recommendations."""
    
    with console.status("[bold green]Optimizing transit..."):
        response = query_llama(SYSTEM_PROMPTS["transit_opt"], query)
    
    console.print(Panel(Markdown(response), title="🚌 Transit Optimization", border_style="blue"))

def run_urban_planning():
    """Assist with urban planning."""
    console.print(Panel("🏗️ Urban Planning Assistant", style="bold green"))
    
    request = get_multiline_input("""Describe the urban planning request:
- Project or area description
- Development proposal
- Community concerns
- Goals and constraints
- Timeline""")
    
    query = f"""Provide urban planning analysis and recommendations.

**REQUEST:**
{request}

Deliver comprehensive urban planning guidance."""
    
    with console.status("[bold green]Analyzing urban planning..."):
        response = query_llama(SYSTEM_PROMPTS["urban_planning"], query)
    
    console.print(Panel(Markdown(response), title="🏗️ Urban Planning Analysis", border_style="cyan"))

def run_citizen_services():
    """Manage citizen services."""
    console.print(Panel("👥 Citizen Services Hub", style="bold green"))
    
    request = get_multiline_input("""Describe the citizen services request:
- Service type or category
- Current issues
- Citizen feedback
- Improvement goals
- Resources available""")
    
    query = f"""Optimize citizen services delivery.

**REQUEST:**
{request}

Provide comprehensive citizen services recommendations."""
    
    with console.status("[bold green]Analyzing citizen services..."):
        response = query_llama(SYSTEM_PROMPTS["citizen_services"], query)
    
    console.print(Panel(Markdown(response), title="👥 Citizen Services Analysis", border_style="magenta"))

def run_infra_monitor():
    """Monitor infrastructure."""
    console.print(Panel("🔧 Infrastructure Monitor", style="bold green"))
    
    request = get_multiline_input("""Describe the infrastructure monitoring request:
- Asset type or system
- Current status/concerns
- Maintenance history
- Priority areas
- Budget constraints""")
    
    query = f"""Monitor and analyze infrastructure status.

**REQUEST:**
{request}

Provide comprehensive infrastructure monitoring recommendations."""
    
    with console.status("[bold green]Monitoring infrastructure..."):
        response = query_llama(SYSTEM_PROMPTS["infra_monitor"], query)
    
    console.print(Panel(Markdown(response), title="🔧 Infrastructure Analysis", border_style="yellow"))

def run_event_mgmt():
    """Manage city events."""
    console.print(Panel("🎉 Event Management System", style="bold green"))
    
    event = get_multiline_input("""Describe the event to manage:
- Event type and name
- Expected attendance
- Location
- Date and duration
- Special requirements""")
    
    query = f"""Plan and coordinate city event management.

**EVENT:**
{event}

Provide comprehensive event management recommendations."""
    
    with console.status("[bold green]Planning event management..."):
        response = query_llama(SYSTEM_PROMPTS["event_mgmt"], query)
    
    console.print(Panel(Markdown(response), title="🎉 Event Management Plan", border_style="magenta"))

def run_city_dashboard():
    """Generate city dashboard."""
    console.print(Panel("📊 City Dashboard Generator", style="bold green"))
    
    focus = get_multiline_input("""Specify dashboard focus areas:
- Sectors to include
- Time period
- Specific KPIs
- Comparison needs
- Audience (executive/operational/public)""")
    
    city_name = Prompt.ask("City name", default="Metro City")
    
    query = f"""Generate a comprehensive city dashboard for {city_name}.

**FOCUS:**
{focus}

**REPORT DATE:** {datetime.now().strftime("%Y-%m-%d")}

Create an executive dashboard with all key metrics and insights."""
    
    with console.status("[bold green]Generating city dashboard..."):
        response = query_llama(SYSTEM_PROMPTS["city_dashboard"], query)
    
    console.print(Panel(Markdown(response), title=f"📊 {city_name} Dashboard", border_style="blue"))

def main():
    """Main application loop."""
    while True:
        display_menu()
        choice = Prompt.ask("\nSelect a module", choices=["0","1","2","3","4","5","6","7","8","9","10"])
        
        if choice == "0":
            console.print("\n[yellow]Thank you for using the Smart City Operating System![/yellow]")
            console.print("[dim]Building smarter cities for a better tomorrow.[/dim]")
            console.print("[dim]Author: Pranay M.[/dim]\n")
            break
        
        try:
            if choice == "1":
                run_traffic_mgmt()
            elif choice == "2":
                run_energy_grid()
            elif choice == "3":
                run_public_safety()
            elif choice == "4":
                run_env_monitor()
            elif choice == "5":
                run_transit_opt()
            elif choice == "6":
                run_urban_planning()
            elif choice == "7":
                run_citizen_services()
            elif choice == "8":
                run_infra_monitor()
            elif choice == "9":
                run_event_mgmt()
            elif choice == "10":
                run_city_dashboard()
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Error: {str(e)}[/red]")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
