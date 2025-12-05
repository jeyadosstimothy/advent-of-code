defmodule Solution do
  def parse_range(str) do
    str |> String.split("-") |> Enum.map(&String.to_integer/1) |> List.to_tuple()
  end

  def parse_input(str) do
    lines = str |> String.split("\n") |> Enum.map(&String.trim/1)
    i = Enum.find_index(lines, fn line -> String.length(line) == 0 end)
    {fresh_ranges, [_ | available]} = Enum.split(lines, i)

    {fresh_ranges |> Enum.map(&Solution.parse_range/1),
     available |> Enum.map(&String.to_integer/1)}
  end

  def is_fresh(id, fresh_ranges) do
    fresh_ranges |> Enum.any?(fn {s, e} -> s <= id and id <= e end)
  end

  def solve_part_1(fresh_ranges, available) do
    available |> Enum.count(&Solution.is_fresh(&1, fresh_ranges))
  end

  def solve_part_2(fresh_ranges) do
    Enum.sort(fresh_ranges)
    |> Enum.reduce([], fn {s, e}, acc ->
      if length(acc) == 0 do
        [{s, e}]
      else
        [{ps, pe} | rem] = acc

        if pe < s do
          [{s, e}] ++ acc
        else
          [{ps, max(e, pe)}] ++ rem
        end
      end
    end)
    |> Enum.reduce(0, fn {s, e}, acc -> acc + e - s + 1 end)
  end
end

{fresh_ranges, available} =
  "inp5.2.txt"
  |> File.read!()
  |> Solution.parse_input()

IO.puts("Part 1:")

Solution.solve_part_1(fresh_ranges, available)
|> IO.inspect()

IO.puts("Part 2:")

Solution.solve_part_2(fresh_ranges)
|> IO.inspect()
