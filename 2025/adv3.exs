defmodule Solution do
  def parse(str) do
    str
    |> String.trim()
    |> String.graphemes()
    |> Enum.map(&String.to_integer/1)
    |> List.to_tuple()
  end

  def calculate_suffix_max(bank) do
    bank
    |> Tuple.to_list()
    |> Enum.reverse()
    |> Enum.scan(&max/2)
    |> Enum.reverse()
    |> List.to_tuple()
  end

  def find_max_part_1(bank) do
    prefix_max = calculate_suffix_max(bank)
    len = tuple_size(bank)

    0..(len - 2)
    |> Enum.map(fn i -> elem(bank, i) * 10 + elem(prefix_max, i + 1) end)
    |> Enum.reduce(&max/2)
  end

  def num_digits(n) do
    n |> Integer.digits() |> length
  end

  def find_max_part_2(bank) do
    len = tuple_size(bank)

    dp =
      Enum.reduce((len - 1)..0//-1, %{}, fn i, dp ->
        len = tuple_size(bank)

        if i == len - 1 do
          %{{i, 1} => elem(bank, i)}
        else
          take_max = min(len - i, 12)

          new_dp =
            for take <- 1..take_max, into: %{} do
              max_value =
                if take == 1 do
                  max(elem(bank, i), Map.get(dp, {i + 1, take}, -1))
                else
                  n = dp[{i + 1, take - 1}]

                  max(
                    elem(bank, i) * 10 ** Solution.num_digits(n) + n,
                    Map.get(dp, {i + 1, take}, -1)
                  )
                end

              {{i, take}, max_value}
            end

          # IO.inspect(new_dp)
          Map.merge(dp, new_dp)
        end
      end)

    dp[{0, 12}]
  end
end

banks =
  "inp3.2.txt"
  |> File.stream!()
  |> Enum.map(&Solution.parse/1)

IO.puts("Part 1:")

banks
|> Enum.map(&Solution.find_max_part_1/1)
|> Enum.reduce(&+/2)
|> IO.puts()

IO.puts("Part 2:")

banks
|> Enum.map(&Solution.find_max_part_2/1)
|> Enum.reduce(&+/2)
|> IO.puts()
