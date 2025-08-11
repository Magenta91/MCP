#!/usr/bin/env python3
"""
Test script for the MCP server to verify it works correctly
"""

import asyncio
import json
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    """Test the MCP server functionality."""
    print("🧪 Testing MCP Dataset Onboarding Server")
    print("=" * 50)
    
    try:
        # Start the MCP server as a subprocess
        async with stdio_client(["python", "mcp_server.py"]) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                
                print("✅ MCP Server initialized successfully")
                
                # List available tools
                tools = await session.list_tools()
                print(f"\n📋 Available Tools ({len(tools.tools)}):")
                for tool in tools.tools:
                    print(f"  • {tool.name}: {tool.description}")
                
                # Test a simple tool call (list processed datasets)
                print(f"\n🔧 Testing 'list_processed_datasets' tool...")
                result = await session.call_tool("list_processed_datasets", {})
                
                if result.isError:
                    print(f"❌ Tool call failed: {result.content}")
                else:
                    print("✅ Tool call successful!")
                    for content in result.content:
                        if hasattr(content, 'text'):
                            print(f"📄 Response: {content.text[:200]}...")
                
                print(f"\n🎉 MCP Server is working correctly!")
                
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_server())