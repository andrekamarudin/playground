# 🎮 Async Programming Playground

A comprehensive demonstration of async programming patterns in Python, showcasing the power of async generators and concurrent HTTP requests.

## 🚀 Features

### Async Patterns Demonstrated

1. **Sequential vs Concurrent Async Generators**
   - Sequential processing (one task at a time)
   - Concurrent processing (all tasks start immediately)
   - Performance comparisons

2. **HTTP Request Patterns with httpx**
   - Sequential HTTP requests
   - Concurrent HTTP requests
   - Batch processing with controlled concurrency
   - Error handling and response processing

3. **Real-world Examples**
   - Fetching multiple URLs concurrently
   - Processing results as they arrive
   - Measuring performance differences

## 📂 Project Structure

```
playground/
├── src/
│   ├── async generator.py      # Original sequential vs concurrent demo
│   ├── async httpx.py          # Simple httpx example
│   └── integrated_async_demo.py # Comprehensive integrated demo
├── tests/
│   └── test_integration.py     # Test suite
├── main.py                     # Entry point
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## 🛠️ Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Install development dependencies (optional):**
   ```bash
   uv sync --extra dev
   ```

## 🎯 Usage

### Run the Complete Demo

```bash
python main.py
```

### Run Individual Examples

**Original async generator demo:**
```bash
python src/"async generator.py"
```

**Simple httpx example:**
```bash
python src/"async httpx.py"
```

**Integrated comprehensive demo:**
```bash
python src/integrated_async_demo.py
```

### Run Tests

**With pytest (recommended):**
```bash
uv run pytest tests/
```

**Simple test runner:**
```bash
python tests/test_integration.py
```

## 📊 What You'll See

The integrated demo showcases three different patterns:

### 1. Sequential Pattern
- Processes URLs one at a time
- Predictable order
- Slower execution (sum of all delays)

### 2. Concurrent Pattern  
- Starts all requests immediately
- Results arrive as they complete (unpredictable order)
- Much faster execution (limited by slowest request)

### 3. Batch Pattern
- Processes URLs in controlled batches
- Balances speed with resource management
- Good for rate-limited APIs

## 🔧 Key Concepts Demonstrated

- **Async Generators**: `AsyncGenerator[T, None]` for streaming results
- **Concurrency Control**: Using `asyncio.as_completed()` for concurrent processing
- **Error Handling**: Graceful handling of failed requests
- **Performance Measurement**: Timing different approaches
- **Resource Management**: Using async context managers (`async with`)

## 📈 Performance Insights

The demo typically shows:
- **Concurrent requests**: 3-10x faster than sequential
- **Batch processing**: Good balance between speed and control
- **Memory efficiency**: Results are yielded as they arrive (streaming)

## 🧪 Testing

The test suite covers:
- Individual URL fetching
- Sequential generator functionality  
- Concurrent generator functionality
- Error handling scenarios

## 💡 Learning Outcomes

After running this playground, you'll understand:

1. When to use sequential vs concurrent async patterns
2. How async generators can stream results efficiently
3. Different strategies for managing concurrent HTTP requests
4. Performance implications of various async patterns
5. How to structure and test async Python code

## 🌟 Next Steps

Try modifying the code to:
- Add more complex error handling
- Implement retry logic for failed requests
- Add rate limiting to respect API constraints
- Stream results to a file or database
- Add progress reporting for long-running operations

---

**Happy async coding!** 🚀