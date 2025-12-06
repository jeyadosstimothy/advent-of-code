defmodule Solution do
  def parse_part_1(file_input) do
    lines = file_input |> String.split("\n") |> Enum.map(&String.trim/1)
    {numbers, operations} = lines |> Enum.map(&String.split/1) |> Enum.split(length(lines) - 1)

    {numbers
     |> Enum.map(fn row -> row |> Enum.map(&String.to_integer/1) end)
     |> Enum.zip()
     |> Enum.map(&Tuple.to_list/1), operations |> hd}
  end

  def operate({col, "+"}) do
    Enum.reduce(col, &+/2)
  end

  def operate({col, "*"}) do
    Enum.reduce(col, &*/2)
  end

  def solve_part_1(file_input) do
    {numbers, operations} = parse_part_1(file_input)

    Enum.zip(numbers, operations)
    |> Enum.map(&Solution.operate/1)
    |> Enum.reduce(&+/2)
  end

  def parse_part_2(file_input) do
    lines =
      file_input
      |> String.split("\n")

    {numbers, operators} =
      lines
      |> Enum.map(&String.graphemes/1)
      |> Enum.split(length(lines) - 1)

    {numbers
     |> Enum.zip()
     |> Enum.map(fn row -> row |> Tuple.to_list() |> List.to_string() |> String.trim() end)
     |> Enum.reverse()
     |> Enum.reduce([[]], fn x, acc ->
       if x == "" do
         [[]] ++ acc
       else
         [prev | rem] = acc
         [[String.to_integer(x)] ++ prev] ++ rem
       end
     end),
     operators
     |> hd
     |> Enum.filter(&(&1 != " "))}
  end

  def solve_part_2(file_input) do
    {numbers, operations} = parse_part_2(file_input)

    Enum.zip(numbers, operations)
    |> Enum.map(&Solution.operate/1)
    |> Enum.reduce(&+/2)
  end
end

file_content = "inp6.2.txt" |> File.read!()

IO.puts("Part 1:")

Solution.solve_part_1(file_content)
|> IO.inspect()

IO.puts("Part 2:")

Solution.solve_part_2(file_content)
|> IO.inspect()
