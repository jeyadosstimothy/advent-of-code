defmodule Solution do
  def parse_line(str) do
    [name | edges] = str |> String.split(" ")
    name = String.trim(name, ":")
    {name, edges}
  end

  def traverse([], _devices, counters) do
    counters
  end

  def traverse([curr | rem], devices, counters) do
    next = Map.get(devices, curr, [])
    curr_count = Map.get(counters, curr, 0)
    traverse(rem ++ next, devices, Map.put(counters, curr, curr_count + 1))
  end

  def solve_part_1(devices, from, to) do
    queue = [from]
    counters = traverse(queue, devices, %{})
    Map.get(counters, to)
  end

  def traverse_part_2(in_degrees, _graph, counters) when map_size(in_degrees) == 0 do
    counters
  end

  def traverse_part_2(in_degrees, graph, counters) do
    nodes_to_remove =
      in_degrees
      |> Enum.filter(fn {_node, in_degree} -> in_degree == 0 end)
      |> Enum.map(fn {node, _in_degree} -> node end)

    matched = ["fft", "dac"]
    |> Enum.filter(fn node -> node in nodes_to_remove end)

    counters = if length(matched) != 0 do
      [first | _] = matched
      %{first => Map.get(counters, first)}
    else
      counters
    end


    new_counters = nodes_to_remove
    |> Enum.flat_map(fn node ->
      Map.get(graph, node, [])
      |> Enum.map(fn child -> {node, child} end)
    end)
    |> Enum.reduce(counters, fn {node, child}, counter_acc ->
      count = Map.get(counter_acc, node, 0)
      child_count = Map.get(counter_acc, child, 0)

      Map.put(counter_acc, child, count + child_count)
    end)

    new_indegrees =
      nodes_to_remove
      |> Enum.flat_map(fn node -> Map.get(graph, node, []) end)
      |> Enum.reduce(in_degrees, fn child, in_degrees_acc ->
        child_in_degree = Map.get(in_degrees_acc, child)
        Map.put(in_degrees_acc, child, child_in_degree - 1)
      end)
      |> Enum.filter(fn {node, _in_degree} -> node not in nodes_to_remove end)
      |> Map.new()

    traverse_part_2(new_indegrees, graph, new_counters)
  end

  def solve_part_2(graph) do
    all_nodes =
      graph
      |> Enum.flat_map(fn {node, children} -> [node] ++ children end)
      |> MapSet.new()

    rev_graph =
      graph
      |> Enum.flat_map(fn {node, children} -> children |> Enum.map(&{&1, node}) end)
      |> Enum.group_by(&elem(&1, 0), &elem(&1, 1))

    in_degrees =
      all_nodes
      |> Map.new(fn node -> {node, Map.get(rev_graph, node, []) |> length()} end)

    traverse_part_2(in_degrees, graph, %{"svr" => 1})
    |> Map.get("out")
  end
end

devices =
  IO.read(:stdio, :eof)
  |> String.split("\n")
  |> Enum.map(&Solution.parse_line/1)
  |> Map.new()

IO.puts("Part 1:")

Solution.solve_part_1(devices, "you", "out")
|> IO.inspect()

IO.puts("Part 2:")

Solution.solve_part_2(devices)
|> IO.inspect(limit: :infinity)
