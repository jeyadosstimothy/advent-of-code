defmodule Solution do
  def enough_space?(gifts, {{l, w}, gift_counts}) do
    gift_space_map =
      gifts
      |> Enum.map(fn {i, gift} -> {i, gift |> Enum.flat_map(& &1) |> Enum.sum()} end)
      |> Map.new()

    available_space = l * w

    required_space =
      gift_counts
      |> Enum.with_index()
      |> Enum.map(fn {count, i} -> count * Map.get(gift_space_map, i) end)
      |> Enum.sum()

    required_space <= available_space
  end

  def solve_part_1(gifts, trees) do
    trees |> Enum.filter(&enough_space?(gifts, &1)) |> length()
  end
end

lines =
  IO.read(:stdio, :eof)
  |> String.split("\n")

gifts =
  lines
  |> Enum.filter(fn line ->
    not Regex.match?(~r/\d+x\d+:( \d+)+/, line) and String.length(line) != 0
  end)
  |> Enum.reduce(%{}, fn line, acc ->
    if Regex.match?(~r/\d+:/, line) do
      Map.put(acc, line |> String.trim(":") |> String.to_integer(), [])
    else
      {idx, rows} = acc |> Enum.sort(:desc) |> hd
      row = line |> String.to_charlist() |> Enum.map(fn c -> if(c == ?#, do: 1, else: 0) end)
      Map.put(acc, idx, rows ++ [row])
    end
  end)

trees =
  lines
  |> Enum.filter(fn line -> Regex.match?(~r/\d+x\d+:( \d+)+/, line) end)
  |> Enum.map(fn line ->
    {dimensions, counts} = line |> String.split(": ") |> List.to_tuple()

    dimensions =
      dimensions |> String.split("x") |> Enum.map(&String.to_integer/1) |> List.to_tuple()

    counts = counts |> String.trim() |> String.split(" ") |> Enum.map(&String.to_integer/1)
    {dimensions, counts}
  end)

IO.puts("Part 1:")

Solution.solve_part_1(gifts, trees)
|> IO.inspect()
