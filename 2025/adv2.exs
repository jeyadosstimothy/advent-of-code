defmodule Solution do
  def parse_range(range_str) do
    range_str
    |> String.split("-")
    |> Enum.map(&String.to_integer/1)
    |> List.to_tuple()
  end

  def parse(str) do
    str
    |> String.trim()
    |> String.split(",")
    |> Enum.map(&Solution.parse_range/1)
  end

  def split_half(n) do
    digits = Solution.num_digits(n)
    divisor = 10 ** div(digits, 2)
    {div(n, divisor), rem(n, divisor)}
  end

  def duplicate(n) do
    digits = Solution.num_digits(n)
    n * 10 ** digits + n
  end

  def num_digits(n) do
    n |> Integer.digits() |> length
  end

  def find_invalid_product_ids_part_1(range) do
    {from, to} = range

    {from_len, to_len} =
      range |> Tuple.to_list() |> Enum.map(&Solution.num_digits/1) |> List.to_tuple()

    gen_start =
      if rem(from_len, 2) == 0 do
        {l, r} = Solution.split_half(from)
        if(l < r, do: l + 1, else: l)
      else
        10 ** div(from_len, 2)
      end

    gen_end =
      if rem(to_len, 2) == 0 do
        {l, r} = Solution.split_half(to)
        if(l <= r, do: l, else: l - 1)
      else
        10 ** div(to_len, 2) - 1
      end

    # IO.puts("#{from}-#{to}: #{gen_start}..#{gen_end}")
    if gen_start <= gen_end do
      gen_start..gen_end
      |> Enum.map(&Solution.duplicate/1)
    else
      []
    end
  end

  def repeat(n, times) do
    digits = Solution.num_digits(n)
    1..times |> Enum.reduce(0, fn _, v -> v * 10 ** digits + n end)
  end

  def in_range({from, to}, x) do
    x >= from and x <= to
  end

  def generate_invalid_product_ids(repeat_count, ranges, max_value) do
    Stream.iterate(1, &(&1 + 1))
    |> Enum.reduce_while([], fn generator, acc ->
      num = Solution.repeat(generator, repeat_count)
      # IO.puts("#{generator} ** #{repeat_count}")

      if num > max_value do
        {:halt, acc}
      else
        in_any_range? = ranges |> Enum.any?(&Solution.in_range(&1, num))

        new_acc =
          if in_any_range? do
            [num] ++ acc
          else
            acc
          end

        {:cont, new_acc}
      end
    end)
  end

  def find_invalid_product_ids_part_2(ranges) do
    max_value = ranges |> Enum.map(&elem(&1, 1)) |> Enum.reduce(&max/2)
    max_value_digits = Solution.num_digits(max_value)

    2..max_value_digits
    |> Enum.flat_map(&Solution.generate_invalid_product_ids(&1, ranges, max_value))
    |> Enum.into(MapSet.new())
  end
end

ranges =
  "inp2.2.txt"
  |> File.stream!()
  |> Enum.map(&Solution.parse/1)
  |> hd

IO.puts("Part 1:")

ranges
|> Enum.flat_map(&Solution.find_invalid_product_ids_part_1/1)
|> Enum.reduce(0, &+/2)
|> IO.puts()

IO.puts("Part 2:")

ranges
|> Solution.find_invalid_product_ids_part_2()
|> Enum.reduce(0, &+/2)
|> IO.puts()
