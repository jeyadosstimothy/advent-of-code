defmodule Solution do
  def parse_line(str) do
    String.trim(str)
  end

  defp add_boundary_space(graph) do
    new_rows = Enum.map(graph, &("." <> &1 <> "."))
    num_columns = new_rows |> hd() |> String.length()
    blank_row = String.duplicate(".", num_columns)

    [blank_row] ++ new_rows ++ [blank_row]
  end

  def parse_graph(graph) do
    graph_boundary_space = add_boundary_space(graph)

    graph_map =
      graph_boundary_space
      |> Enum.with_index()
      |> Enum.flat_map(fn {row, i} ->
        row
        |> String.graphemes()
        |> Enum.with_index()
        |> Enum.map(fn {char, j} -> {{i, j}, char} end)
      end)
      |> Enum.into(%{})

    bounds = {graph_boundary_space |> length, graph_boundary_space |> hd |> String.length()}

    {graph_map, bounds}
  end

  def char_locations(graph) do
    Enum.group_by(graph, fn {_pos, c} -> c end, fn {pos, _c} -> pos end)
  end

  def within_bounds({i, j}, {bi, bj}) do
    i >= 0 and i < bi and j >= 0 and j < bj
  end

  def neighbours({i, j}, bounds) do
    [{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}]
    |> Enum.map(fn {di, dj} -> {i + di, j + dj} end)
    |> Enum.filter(&within_bounds(&1, bounds))
  end

  def solve_part_1(graph, bounds) do
    char_locations(graph)
    |> Map.get("@")
    |> Enum.map(fn pos ->
      {pos,
       Solution.neighbours(pos, bounds)
       |> Enum.count(&(graph[&1] == "@"))}
    end)
    |> Enum.count(fn {_pos, n} -> n < 4 end)
  end

  def print(rolls, {bi, bj}) do
    Enum.each(0..bi, fn i ->
      Enum.map(0..bj, fn j ->
        cond do
          Map.has_key?(rolls, {i, j}) -> "@"
          true -> "."
        end
      end)
      |> List.to_string()
      |> IO.puts()
    end)

    IO.puts("")
  end

  def recurse(rolls, bounds, removed_count) do
    # IO.puts("#{removed_count}")
    # Solution.print(rolls, bounds)

    to_remove =
      Enum.filter(rolls, fn {_pos, n} -> n < 4 end)
      |> Enum.map(fn {pos, _n} -> pos end)
      |> MapSet.new()

    if MapSet.size(to_remove) == 0 do
      removed_count
    else
      remaining_rolls = Map.drop(rolls, MapSet.to_list(to_remove))

      neighbours_to_update =
        Enum.flat_map(to_remove, &Solution.neighbours(&1, bounds))
        |> Enum.filter(&Map.has_key?(remaining_rolls, &1))
        |> Enum.frequencies()

      new_rolls =
        Enum.map(remaining_rolls, fn {pos, n} ->
          {pos, n - Map.get(neighbours_to_update, pos, 0)}
        end)
        |> Map.new()

      recurse(new_rolls, bounds, removed_count + MapSet.size(to_remove))
    end
  end

  def solve_part_2(graph, bounds) do
    rolls =
      char_locations(graph)
      |> Map.get("@")
      |> Enum.map(fn pos ->
        neighbours =
          Solution.neighbours(pos, bounds)
          |> Enum.filter(&(graph[&1] == "@"))
          |> length()

        {pos, neighbours}
      end)
      |> Map.new()

    recurse(rolls, bounds, 0)
  end
end

{graph, bounds} =
  "inp4.2.txt"
  |> File.stream!()
  |> Enum.map(&Solution.parse_line/1)
  |> Solution.parse_graph()

IO.puts("Part 1:")

Solution.solve_part_1(graph, bounds)
|> IO.inspect()

IO.puts("Part 2:")

Solution.solve_part_2(graph, bounds)
|> IO.inspect()
