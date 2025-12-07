defmodule Solution do
  def parse_line(str) do
    String.trim(str)
  end

  def parse_graph(graph) do
    graph_map =
      graph
      |> Enum.with_index()
      |> Enum.flat_map(fn {row, i} ->
        row
        |> String.graphemes()
        |> Enum.with_index()
        |> Enum.map(fn {char, j} -> {{i, j}, char} end)
      end)
      |> Enum.into(%{})

    bounds = {graph |> length, graph |> hd |> String.length()}

    {graph_map, bounds}
  end

  def char_locations(graph) do
    Enum.group_by(graph, fn {_pos, c} -> c end, fn {pos, _c} -> pos end)
  end

  def split(j, bj) do
    [-1, 1]
    |> Enum.map(&(j + &1))
    |> Enum.filter(&(&1 >= 0 and &1 < bj))
  end

  def solve_part_1(graph, {bi, bj}) do
    locations = char_locations(graph)

    {{si, sj}, splitters} =
      {Map.get(locations, "S") |> hd, Map.get(locations, "^") |> MapSet.new()}

    si..(bi - 1)
    |> Enum.reduce({[sj], 0}, fn i, {js, count} ->
      {new_js, splits} =
        js
        |> Enum.flat_map_reduce(0, fn j, acc ->
          if MapSet.member?(splitters, {i, j}) do
            {Solution.split(j, bj), acc + 1}
          else
            {[j], acc}
          end
        end)

      {MapSet.new(new_js), count + splits}
    end)
    |> elem(1)
  end

  def solve_part_2(graph, {bi, bj}) do
    locations = char_locations(graph)

    {{si, sj}, splitters} =
      {Map.get(locations, "S") |> hd, Map.get(locations, "^") |> MapSet.new()}

    si..(bi - 1)
    |> Enum.reduce([{sj, 1}], fn i, jcs ->
      jcs
      |> Enum.flat_map(fn {j, c} ->
        if MapSet.member?(splitters, {i, j}) do
          Solution.split(j, bj) |> Enum.map(&{&1, c})
        else
          [{j, c}]
        end
      end)
      |> Enum.group_by(fn {j, c} -> j end, fn {j, c} -> c end)
      |> Enum.map(fn {j, cs} -> {j, Enum.sum(cs)} end)
    end)
    |> Enum.map(fn {j, c} -> c end)
    |> Enum.sum()
  end
end

{graph, bounds} =
  "inp7.2.txt"
  |> File.stream!()
  |> Enum.map(&Solution.parse_line/1)
  |> Solution.parse_graph()

IO.puts("Part 1:")

Solution.solve_part_1(graph, bounds)
|> IO.inspect()

IO.puts("Part 2:")

Solution.solve_part_2(graph, bounds)
|> IO.inspect()
