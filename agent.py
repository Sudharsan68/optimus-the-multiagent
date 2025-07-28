import os
from agno.agent import Agent, RunResponse
from agno.models.openrouter import OpenRouter
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools




import streamlit as st

# Streamlit sidebar input for API key
st.sidebar.title("API Configuration")
api_key = st.sidebar.text_input("Enter your OpenRouter API key: ", type="password")


# Sidebar agent selector
st.sidebar.title("🤖 Agent Selector")
agent_choice = st.sidebar.radio("Choose Agent:", ("Multi Agent", "Finance Agent", "Web Search Agent"))
# Web search agent 

web_search_agent = Agent(
    name="web search agent",
    role="search the web for the information",
    model=OpenRouter(id="gpt-4o-mini", api_key=api_key),  # Use the OpenRouter API key from user input
    tools=[DuckDuckGoTools()],
    instructions=["always include sources"],
    show_tool_calls=True,
    markdown=True
)

# Finance agent
finance_agent = Agent(
    name="Finance AI agent",
    model=OpenRouter(id="gpt-4o-mini", api_key=api_key),  # Use the OpenRouter API key from user input
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True)],
    instructions=["use tables to display data"],
    show_tool_calls=True,
    markdown=True
)

multi_agent = Agent(
    team=[finance_agent, web_search_agent],
    name="multi agent",
    model=OpenRouter(id="gpt-4o-mini", api_key=api_key),  # Use the OpenRouter API key from user input
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True)],
    instructions=["always include sources","use tables to display data"],
    show_tool_calls=True,
    markdown=True
)

st.title("Optimus- A MULTI UTILITY USER INTERFACE ")

#question = st.text_input("Enter your question: ")
#if st.button("Submit"):
#    response = multi_agent.run(question)
#    st.write(response.content)
question = st.text_input("Enter your question:")
if st.button("Submit"):
    if agent_choice == "Multi Agent":
        response = multi_agent.run(question)
    elif agent_choice == "Finance Agent":
        response = finance_agent.run(question)
    elif agent_choice == "Web Search Agent":
        response = web_search_agent.run(question)
    else:
        response = None
    if response:
        st.write(response.content)
    else:
        st.warning("⚠️ Please enter your OpenRouter API key to continue.")
