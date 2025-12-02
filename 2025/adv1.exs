defmodule Solution do
  def parse_line(s) do
    {direction, num_str} =
      s
      |> String.trim()
      |> String.split_at(1)

    {direction, String.to_integer(num_str)}
  end

  def move_dial("L", offset, curr) do
    Integer.mod(curr - offset, 100)
  end

  def move_dial("R", offset, curr) do
    Integer.mod(curr + offset, 100)
  end

  def move_dial_reducer_part_1({direction, offset}, {curr, ans}) do
    new = move_dial(direction, offset, curr)

    # IO.puts("#{direction}#{offset}: #{new} - #{ans}")

    {new, if(new == 0, do: ans + 1, else: ans)}
  end

  def crossed_zero?("L", curr, offset) do
    curr - offset <= 0
  end

  def crossed_zero?("R", curr, offset) do
    curr + offset >= 100
  end

  def move_dial_reducer_part_2({direction, offset}, {curr, ans}) do
    count = div(offset, 100)
    rem_offset = rem(offset, 100)

    crossed_zero =
      rem_offset != 0 and curr != 0 and Solution.crossed_zero?(direction, curr, rem_offset)

    crossed = count + if(crossed_zero, do: 1, else: 0)

    new_ans = ans + crossed

    new = move_dial(direction, offset, curr)

    # IO.puts("#{direction}#{offset} -> #{new} : #{crossed} = #{new_ans}")

    {new, new_ans}
  end
end

instructions =
  "inp1.2.txt"
  |> File.stream!()
  |> Stream.map(&Solution.parse_line/1)

IO.puts("Part 1:")

instructions
|> Enum.reduce({50, 0}, &Solution.move_dial_reducer_part_1/2)
|> IO.inspect()

IO.puts("Part 2:")

instructions
|> Enum.reduce({50, 0}, &Solution.move_dial_reducer_part_2/2)
|> IO.inspect()
