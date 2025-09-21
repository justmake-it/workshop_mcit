# Google Agent Development Kit (ADK) Framework Overview

## Introduction

Google's Agent Development Kit (ADK) is a comprehensive, open-source, code-first Python toolkit designed for building, evaluating, and deploying AI agents. ADK emphasizes testability, modularity, and deployment flexibility, making agent development similar to traditional software development.

Repositories to use when using deepwiki or web:

1. (samples)[https://github.com/google/adk-samples]
2. (core)[https://github.com/google/adk-python]

## Core Philosophy

ADK is built on several key principles:

- **Code-First Development**: Agents are defined directly in Python code, enabling flexibility, testability, and versioning
- **Model-Agnostic**: While optimized for Gemini, ADK supports various LLMs and is compatible with other frameworks
- **Deployment-Agnostic**: Flexible deployment options across Google Cloud services and local environments
- **Modular Architecture**: Supports building complex multi-agent systems through composition

## Core Architecture Components

### 1. Agent System

The Agent System provides core agent abstractions and implementations:

#### BaseAgent

The foundational class for all agents that can be extended to create different agent types.

#### LlmAgent (Agent)

Agents that use Large Language Models for reasoning, natural language understanding, and decision-making:

```python
from google.adk.agents import LlmAgent
from google.adk.tools import google_search

root_agent = LlmAgent(
    name="search_assistant",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant. Answer user questions using Google Search when needed.",
    description="An assistant that can search the web.",
    tools=[google_search]
)
```

#### Workflow Agents

Deterministic agents that control execution flow without using LLMs:

- **SequentialAgent**: Executes sub-agents one after another in order
- **ParallelAgent**: Executes multiple sub-agents concurrently
- **LoopAgent**: Repeatedly executes sub-agents until a termination condition is met

```python
from google.adk.agents import SequentialAgent, ParallelAgent

# Multi-agent system example
coordinator = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash",
    description="I coordinate greetings and tasks.",
    sub_agents=[greeter, task_executor]
)
```

#### Custom Agents

Created by extending `BaseAgent` and implementing unique logic in the `_run_async_impl` method.

### 2. Execution Engine

#### Runner

Orchestrates the "Reason-Act" loop, manages LLM calls, and executes tools.

#### AgentLoader

Responsible for loading agents during execution.

### 3. Tool Integration

ADK provides an extensible tool ecosystem:

- **OpenAPIToolset**: For integrating with REST APIs
- **MCPToolset**: For Model Context Protocol integration
- **GoogleAPIToolset**: For integrating with Google Cloud APIs
- Built-in tools: `google_search`, `vertex_ai_search`

```python
from google.adk.tools import google_search, vertex_ai_search

tools = [google_search, vertex_ai_search]
```

### 4. Services Layer

Manages state and persistence:

#### SessionService

Manages conversation state for continuous dialogues. See [detailed SessionService documentation](#sessionservice---short-term-memory) below.

- `InMemorySessionService`
- `DatabaseSessionService`
- `VertexAiSessionService`

#### MemoryService

Provides long-term recall across different sessions. See [detailed MemoryService documentation](#memoryservice---long-term-memory) below.

- `InMemoryMemoryService`
- `VertexAiMemoryService`

#### ArtifactService

Manages non-textual data like files:

- `InMemoryArtifactService`
- `GCSArtifactService`

### 5. Memory Management

ADK provides comprehensive memory management through two complementary services that handle different aspects of conversational AI memory. For detailed information, see the [official ADK documentation on sessions](https://google.github.io/adk-docs/sessions/).

#### Memory Management Overview

ADK distinguishes between two types of memory:

1. **Short-term Memory (SessionService)**: Manages the current conversation context, including message history and temporary state within a single interaction
2. **Long-term Memory (MemoryService)**: Provides persistent knowledge storage and retrieval across multiple conversations

These services work together through the `InvocationContext`, allowing agents to maintain both immediate conversational awareness and access to historical knowledge.

#### SessionService - Short-term Memory

The SessionService manages conversation threads through Session objects. Each session represents a single interaction between a user and the agent system. For detailed documentation, see [SessionService guide](https://google.github.io/adk-docs/sessions/session/).

**Core APIs**:

```python
# Create a new conversation
session = await session_service.create_session(
    app_name='my_app',
    user_id='test_user',
    state={'initial_context': 'value'}
)

# Retrieve existing session
session = await session_service.get_session(
    app_name='my_app',
    user_id='test_user',
    session_id='session_123'
)

# List user's sessions
sessions = await session_service.list_sessions(
    app_name='my_app',
    user_id='test_user'
)

# Update session with new event
await session_service.append_event(session=session, event=event)

# Delete session
await session_service.delete_session(
    app_name='my_app',
    user_id='test_user',
    session_id='session_123'
)
```

**State Hierarchy**:

ADK implements a four-tier state system using prefix-based scoping:

```python
event.actions.state_delta = {
    "app:theme": "dark",              # Global app state - shared by all users
    "user:language": "en",            # User state - shared across user's sessions
    "cart_items": ["item1", "item2"], # Session state - specific to this conversation
    "temp:cache_key": "xyz123"        # Ephemeral state - not persisted
}
```

- **`app:`** - Application-wide state shared across all users and sessions
- **`user:`** - User-specific state persisted across all sessions for that user
- **No prefix** - Session-specific state isolated to the current conversation
- **`temp:`** - Temporary state that is not persisted to storage

**Implementations**:

1. **InMemorySessionService**
   - Stores data in application memory
   - No persistence (data lost on restart)
   - Best for: Local development and testing
2. **DatabaseSessionService** (Python only)
   - Uses SQLAlchemy for relational database storage
   - Supports: PostgreSQL, MySQL, SQLite
   - Best for: Production environments requiring persistence
3. **VertexAiSessionService**
   - Integrates with Google Cloud Vertex AI
   - Managed session storage
   - Best for: Cloud-native deployments

#### MemoryService - Long-term Memory

The MemoryService provides persistent knowledge storage and semantic search capabilities across conversations. For implementation details, see [MemoryService guide](https://google.github.io/adk-docs/sessions/memory/).

**Core APIs**:

```python
# Add completed session to memory
await memory_service.add_session_to_memory(session)

# Search memory for relevant information
search_results = await memory_service.search_memory(
    app_name='my_app',
    user_id='test_user',
    query='previous product recommendations'
)
```

**Implementations**:

1. **InMemoryMemoryService**
   - Basic keyword matching
   - No persistence
   - Best for: Prototyping and testing
2. **VertexAiMemoryBankService**
   - Semantic search capabilities
   - Automatic memory extraction and consolidation
   - Requirements:
     ```bash
     export GOOGLE_CLOUD_PROJECT="project-id"
     export GOOGLE_CLOUD_LOCATION="us-central1"
     ```
   - Best for: Production with intelligent memory management
3. **VertexAiRagMemoryService**
   - RAG corpus integration
   - Document-based memory storage
   - Best for: Knowledge-intensive applications

#### Practical Integration

Agents access memory services through the `InvocationContext`. For more details on context management, see [Context documentation](https://google.github.io/adk-docs/context/).

**Accessing Services in Agents**:

```python
class MyAgent(BaseAgent):
    async def _run_async_impl(self, ctx: InvocationContext) -> None:
        # Access SessionService
        session = ctx.session
        await ctx.session_service.append_event(session, event)

        # Access MemoryService (if configured)
        if ctx.memory_service:
            results = await ctx.memory_service.search_memory(
                app_name='my_app',
                user_id=session.user_id,
                query='relevant context'
            )
```

**In Tools via ToolContext**:

```python
@tool
async def search_knowledge(query: str, tool_context: ToolContext) -> str:
    """Search long-term memory for information."""
    search_results = await tool_context.search_memory(query)
    return format_results(search_results)
```

**Configuration**:

Via CLI:

```bash
# Configure memory service
adk run my_agent --memory_service_uri="agentengine://1234567890"

# Or for local development
adk run my_agent --memory_service_uri="inmemory://"
```

Via Environment:

```bash
export MEMORY_SERVICE_URI="vertexai://project-id/location/memory-bank-id"
```

**State Update Pattern**:

```python
# Create event with state updates
event = Event(
    author='assistant',
    content=response_content,
    actions=EventActions(
        state_delta={
            'app:last_update': datetime.now().isoformat(),
            'user:preferences': updated_preferences,
            'conversation_topic': extracted_topic,
            'temp:processing_time': 0.5
        }
    )
)

# Append event - automatically updates session state
await session_service.append_event(session, event)
```

### 6. Evaluation System

Provides capabilities for agent performance evaluation:

- **TrajectoryEvaluator**: Evaluates the sequence of actions taken by an agent
- **ResponseEvaluator**: Evaluates the final responses generated by an agent
- **SafetyEvaluatorV1**: Evaluates agent responses for safety
- **MetricEvaluatorRegistry**: Registers and manages different metric evaluators

### 6. Development Interface

#### ADK CLI

Command-line interface for creating, running, evaluating, and deploying agents:

```bash
# Create a new agent
adk create my_first_agent

# Run agent locally
adk run my_first_agent

# Start web development UI
adk web my_first_agent

# Deploy to Cloud Run
adk deploy cloud_run --project my-project --region us-central1 my_first_agent
```

#### Development Web UI

Angular + FastAPI application for testing, evaluating, debugging, and showcasing agents.

## Agent Creation and Development

### Basic Agent Structure

When creating an agent with `adk create`, the basic structure includes:

```python
from google.adk.agents import LlmAgent
from google.adk.tools import google_search

root_agent = LlmAgent(
    name="my_agent",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant.",
    description="Agent description",
    tools=[google_search]
)
```

### Structured Input/Output

ADK agents support structured input and output schemas using Pydantic BaseModel, enabling predictable data formats essential for multi-agent systems and API integrations.

For detailed information, see the [official ADK documentation on LLM agents](https://google.github.io/adk-docs/agents/llm-agents/).

#### Schema Definition

```python
from pydantic import BaseModel
from google.adk.agents import LlmAgent

class QueryInput(BaseModel):
    query: str
    max_results: int = 5

class SearchResult(BaseModel):
    title: str
    summary: str
    relevance_score: float

# Agent with structured I/O
structured_agent = LlmAgent(
    name="structured_search",
    model="gemini-2.0-flash",
    input_schema=QueryInput,
    output_schema=SearchResult,
    instruction="""You are a search assistant.

    IMPORTANT: Your response must be a JSON object with the following fields:
    - title: The main title of the search result
    - summary: A brief summary of the content
    - relevance_score: A float between 0 and 1 indicating relevance

    Return ONLY valid JSON matching this structure."""
)
```

#### Important Limitations and Solutions

1. **Tools and Structured Output**: Originally, agents with `output_schema` couldn't use tools. ADK now provides an automatic workaround using `SetModelResponseTool`.

2. **Official Pattern**: When an agent has both `output_schema` and `tools`, ADK automatically:
   - Injects a `set_model_response` tool
   - Adds instructions for the LLM to use this tool for final output

3. **Critical Warning - generate_content_config Conflicts**: 
   - When using `output_schema`, ADK automatically handles `response_mime_type`
   - Adding `generate_content_config` can cause conflicts and JSON parsing errors
   - The agent may return text like "Here is the JSON requested:" before the JSON
   - Solution: Remove `generate_content_config` when using `output_schema`

```python
from pydantic import BaseModel
from google.adk.agents import LlmAgent
from google.adk.tools import search_wikipedia, get_current_year

class PersonInfo(BaseModel):
    name: str
    birth_year: int
    occupation: str

# This now works - ADK handles the tool/schema integration
agent_with_both = LlmAgent(
    name="person_info_agent",
    model="gemini-2.5-pro",
    output_schema=PersonInfo,
    tools=[search_wikipedia, get_current_year],
    instruction="""Research information about the person.

    Use the available tools to gather accurate information.

    IMPORTANT: Always use the set_model_response tool to provide
    your final answer in the required JSON structure:
    {
        "name": "string",
        "birth_year": integer,
        "occupation": "string"
    }"""
)
```

3. **Alternative Pattern** (if the automatic workaround has issues):

```python
# Use separate agents in a pipeline
research_agent = LlmAgent(
    name="researcher",
    model="gemini-2.0-flash",
    tools=[search_wikipedia],
    instruction="Research and gather information."
)

formatter_agent = LlmAgent(
    name="formatter",
    model="gemini-2.0-flash",
    output_schema=PersonInfo,
    instruction="Format the information into the required JSON structure."
)

# Combine in sequence
from google.adk.agents import SequentialAgent
pipeline = SequentialAgent(
    name="research_pipeline",
    sub_agents=[research_agent, formatter_agent]
)
```

### Best Practices for Deterministic JSON Output

To ensure agents produce reliable, deterministic JSON output:

#### 1. Use the "Raw JSON Object" Pattern

**Based on ADK samples**, the most reliable pattern for JSON output includes this specific language:

```python
# Proven pattern from ADK samples
instruction = """[Your task description]

Your response must be a single, raw JSON object validating against the 'SchemaName' schema."""
```

This pattern has been tested extensively in ADK samples and prevents common issues like extra text before JSON.

#### 2. Explicit Prompt Instructions

**Always include explicit JSON format instructions in your prompt**, even when using `output_schema`:

```python
# Good practice
instruction = """You are a data extraction agent.

IMPORTANT: You must ALWAYS return your response as a JSON object with this exact structure:
{
    "entity_name": "string",
    "entity_type": "string",
    "confidence": 0.0 to 1.0
}

Do not include any text outside the JSON object."""

# Even better - include an example
instruction = """Extract entities from text.

You must return JSON in this exact format:
{
    "entity_name": "Apple Inc.",
    "entity_type": "ORGANIZATION",
    "confidence": 0.95
}

ONLY return valid JSON. No additional text."""
```

#### 2. Temperature Settings

Use lower temperature for more deterministic outputs:

```python
# WARNING: Do NOT use generate_content_config with output_schema
# This can cause conflicts and JSON parsing errors

structured_agent = LlmAgent(
    name="deterministic_agent",
    model="gemini-2.0-flash",
    output_schema=MySchema,
    # generate_content_config removed - causes conflicts with output_schema
    instruction="""[Your task description]
    
    Your response must be a single, raw JSON object validating against the 'MySchema' schema."""
)
```

#### 3. Error Handling

Always implement fallback mechanisms:

```python
import json

try:
    response = await agent.run(context)
    parsed_data = json.loads(response.messages[-1].text)
except json.JSONDecodeError:
    # Fallback to raw text or retry
    logger.warning("Failed to parse JSON, using raw response")
    parsed_data = {"raw_response": response.messages[-1].text}
```

#### 4. Schema Complexity

Start simple and gradually increase complexity:

```python
# Start with simple schemas
class SimpleOutput(BaseModel):
    result: str
    confidence: float

# Before moving to complex ones
class ComplexOutput(BaseModel):
    results: List[SearchResult]
    metadata: Dict[str, Any]
    processing_stats: ProcessingInfo
```

### Installation

```bash
# Stable release
pip install google-adk

# Development version
pip install git+https://github.com/google/adk-python.git@main
```

## Deployment Options

### Google Cloud Run

```bash
adk deploy cloud_run \
  --project my-gcp-project \
  --region us-central1 \
  --service_name my-agent-service \
  my_first_agent
```

### Vertex AI Agent Engine

```bash
adk deploy agent_engine \
  --project my-gcp-project \
  --region us-central1 \
  --staging_bucket gs://my-staging-bucket \
  --display_name "My Agent" \
  my_first_agent
```

### Google Kubernetes Engine (GKE)

```bash
adk deploy gke \
  --project=[project] \
  --region=[region] \
  --cluster_name=[cluster_name] \
  path/to/my_agent
```

### Local Development

```bash
# Interactive CLI
adk run my_agent

# Web-based development UI
adk web my_agent
```

## Key Features and Capabilities

### 1. Multi-Agent Systems

- Support for agent hierarchies with parent-child relationships
- Agent communication through the Agent2Agent (A2A) protocol
- Flexible composition of specialized agents

### 2. Context Management

Uses `InvocationContext` to bundle information during operations:

- Session state management (see [Memory Management](#memory-management))
- Data passing between agents
- Service access (Artifact, Memory, Authentication)
- Identity tracking

### 3. Evaluation and Testing

- Unit tests and integration tests
- ADK Evaluation Framework with JSON test cases
- Metrics like `tool_trajectory_avg_score` and `response_match_score`

### 4. Tool Ecosystem

- Pre-built tools for common tasks
- Custom function creation
- OpenAPI specification integration
- Third-party library integration

## Agent Execution Flow

1. **User Input** → Processed by `InvocationContext`
2. **Runner.run_async()** → Orchestrates the process
3. **AgentLoader.load_agent()** → Loads the `BaseAgent` instance
4. **LlmAgent.run()** → Interacts with LLM APIs (Gemini/LiteLLM)
5. **Tool Execution** → Utilizes services for state management
6. **Event Streaming** → Returns results to user
7. **Optional Evaluation** → Triggered by evaluators

## Integration with Workshop Framework

In the context of the AgentFlow AI workshop series, ADK provides:

1. **Foundation for Agent Development**: Structured approach to building the Market Researcher, Content Creator, and Outreach Specialist agents

2. **Deployment Pipeline**: Seamless deployment from development to production using Google Cloud services

3. **Evaluation Framework**: Built-in capabilities to assess agent performance and iterate on improvements

4. **Multi-Agent Orchestration**: Support for the compounding effect where agents work together

## Comparison with Gemini CLI

While the workshop scenarios focus on Gemini CLI, ADK provides:

- More structured agent development patterns
- Production-ready deployment capabilities
- Comprehensive evaluation frameworks
- Multi-agent system support

ADK can be seen as the production framework that complements the rapid prototyping capabilities of Gemini CLI.

## Best Practices

1. **Start Simple**: Begin with single-purpose agents before building complex multi-agent systems
2. **Use Appropriate Agent Types**: Choose LlmAgent for reasoning tasks, Workflow Agents for structured processes
3. **Implement Proper Evaluation**: Use the evaluation framework to continuously improve agent performance
4. **Leverage Services**: Utilize SessionService and MemoryService for stateful applications (see [Memory Management](#memory-management))
5. **Design for Deployment**: Consider deployment requirements early in the development process
6. **Template Variable Syntax**: Use single braces `{variable}` not double braces `{{variable}}` in ADK templates
7. **Research ADK Patterns**: Always check ADK samples repository for proven patterns before implementing

## Debugging Best Practices

When encountering issues with ADK agents:

1. **Use deepwiki for Repository Research**: 
   - Search `google/adk-python` for core framework patterns
   - Search `google/adk-samples` for proven implementation examples
   - These repositories contain tested patterns that work reliably

2. **Common JSON Output Issues**:
   - If agents return text before JSON, check for `generate_content_config` conflicts
   - Use the "raw JSON object" pattern from ADK samples
   - Verify template variables use single braces: `{variable}`

3. **Multi-Agent Pipeline Issues**:
   - Ensure output_key from one agent matches template variable in the next
   - Use descriptive output_key names to avoid confusion
   - Test each agent individually before combining in pipelines

## Resources

- **Documentation**: https://google.github.io/adk-docs/
- **GitHub Repository**: https://github.com/google/adk-python
- **ADK Samples**: https://github.com/google/adk-samples
- **Installation**: `pip install google-adk`
- **Weekly Release Cadence**: Regular updates and improvements

## Conclusion

Google ADK represents a mature, production-ready framework for building AI agents that can scale from simple single-purpose tools to complex multi-agent systems. Its code-first approach, deployment flexibility, and comprehensive evaluation capabilities make it an ideal choice for building the AI agents described in the AgentFlow AI workshop series.
