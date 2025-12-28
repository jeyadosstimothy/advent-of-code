import Bitwise

Mix.install([
  {:nx, "~> 0.9"},
  {:explorer, "~> 0.11.1"},
  {:heap, "~> 3.0.0"}
])

defmodule Solution do
  def parse_line(str) do
    captures =
      Regex.named_captures(~r/^\[(?<lights>.*)\] (?<buttons>\(.*\) )+\{(?<joltage>.*)\}$/, str)

    %{
      :lights => Map.get(captures, "lights"),
      :buttons =>
        Map.get(captures, "buttons")
        |> String.trim()
        |> String.split()
        |> Enum.map(fn s ->
          s
          |> String.replace(~r/[\(\)]/, "")
          |> String.split(",")
          |> Enum.map(&String.to_integer/1)
        end),
      :joltage =>
        Map.get(captures, "joltage")
        |> String.split(",")
        |> Enum.map(&String.to_integer/1)
        |> List.to_tuple()
    }
  end

  def recurse_part_1([], 0, presses) do
    presses
  end

  def recurse_part_1([], _target, _presses) do
    100
  end

  def recurse_part_1([curr | rem], target, presses) do
    min(
      recurse_part_1(rem, bxor(target, curr), presses + 1),
      recurse_part_1(rem, target, presses)
    )
  end

  def minimum_presses_part_1(%{lights: lights_input, buttons: buttons_input}) do
    mapping = %{
      ?# => "1",
      ?. => "0"
    }

    lights =
      lights_input
      |> String.to_charlist()
      |> Enum.map(&Map.get(mapping, &1))
      |> Enum.reverse()
      |> Enum.join()
      |> String.to_integer(2)

    buttons =
      buttons_input
      |> Enum.map(fn button_lights ->
        button_lights |> Enum.reduce(0, fn i, acc -> acc ||| 1 <<< i end)
      end)

    recurse_part_1(buttons, lights, 0)
  end

  def solve_part_1(machines) do
    machines
    |> Enum.map(&minimum_presses_part_1/1)
    |> Enum.sum()
  end
end

machines =
  IO.read(:stdio, :eof)
  |> String.split("\n")
  |> Enum.map(&Solution.parse_line/1)

IO.puts("Part 1:")

Solution.solve_part_1(machines)
|> IO.puts()
