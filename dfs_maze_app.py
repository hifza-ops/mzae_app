import streamlit as st
import matplotlib.pyplot as plt

# DFS algorithm
def dfs(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    stack = [start]
    visited = [[False]*cols for _ in range(rows)]
    parent = [[None]*cols for _ in range(rows)]
    visited[start[0]][start[1]] = True

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    while stack:
        r, c = stack.pop()
        if (r, c) == goal:
            break
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and maze[nr][nc] == 0:
                stack.append((nr, nc))
                visited[nr][nc] = True
                parent[nr][nc] = (r, c)

    path = []
    curr = goal
    while curr and curr != start:
        path.append(curr)
        curr = parent[curr[0]][curr[1]]
    if curr == start:
        path.append(start)
        path.reverse()
        return path
    return None

# Visualization
def visualize_maze(maze, path, start, goal):
    rows, cols = len(maze), len(maze[0])
    fig, ax = plt.subplots()
    
    for r in range(rows):
        for c in range(cols):
            cell = maze[r][c]
            y = rows - 1 - r
            color = 'black' if cell == 1 else 'white'
            ax.add_patch(plt.Rectangle((c, y), 1, 1, color=color, ec='gray'))

    if path:
        for idx, (r, c) in enumerate(path):
            y = rows - 1 - r
            ax.add_patch(plt.Rectangle((c, y), 1, 1, color='yellow'))
            ax.text(c + 0.5, y + 0.5, str(idx), ha='center', va='center', fontsize=8, color='blue')

    sr, sc = start
    gr, gc = goal
    ys, yg = rows - 1 - sr, rows - 1 - gr
    ax.add_patch(plt.Rectangle((sc, ys), 1, 1, color='green'))
    ax.text(sc + 0.5, ys + 0.5, 'S', ha='center', va='center', fontsize=10, color='white', weight='bold')
    ax.add_patch(plt.Rectangle((gc, yg), 1, 1, color='red'))
    ax.text(gc + 0.5, yg + 0.5, 'G', ha='center', va='center', fontsize=10, color='white', weight='bold')

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.gca().set_aspect('equal')
    plt.title("DFS Maze Solver - Warehouse Robot Simulation")
    return fig

# Streamlit App UI
st.title("🚗 DFS Maze Solver – Warehouse Robot Simulation")
st.write("Simulates a warehouse robot using DFS to find a path from start to goal.")

rows = st.number_input("Enter number of rows", min_value=2, max_value=20, value=5)
cols = st.number_input("Enter number of columns", min_value=2, max_value=20, value=5)

st.markdown("**Enter the maze grid (0 = path, 1 = wall). One row per line:**")
maze_text = st.text_area("Maze input", "0 0 1 0 0\n1 0 1 0 1\n0 0 0 0 0\n1 1 1 1 0\n0 0 0 0 0", height=150)

start_input = st.text_input("Start position (row,col)", "0,0")
goal_input = st.text_input("Goal position (row,col)", f"{rows-1},{cols-1}")

if st.button("Solve with DFS"):
    try:
        maze = [list(map(int, row.split())) for row in maze_text.strip().split('\n')]
        start = tuple(map(int, start_input.split(',')))
        goal = tuple(map(int, goal_input.split(',')))

        if not (0 <= start[0] < rows and 0 <= start[1] < cols and
                0 <= goal[0] < rows and 0 <= goal[1] < cols):
            st.error("Start or goal is outside the maze!")
        else:
            path = dfs(maze, start, goal)
            if path:
                st.success("✅ Path found!")
                st.write("Path:", path)
                fig = visualize_maze(maze, path, start, goal)
                st.pyplot(fig)
            else:
                st.warning("❌ No path found.")
    except Exception as e:
        st.error(f"Error: {e}")
