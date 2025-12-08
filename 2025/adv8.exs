defmodule DSU do
  def new() do
    %{jn_to_circuit: %{}, circuit_to_jns: %{}}
  end

  defp new(jn_to_circuit, circuit_to_jns) do
    %{jn_to_circuit: jn_to_circuit, circuit_to_jns: circuit_to_jns}
  end

  def create_connection(dsu, jn1, jn2) do
    max_ct = dsu[:circuit_to_jns] |> Map.keys() |> Enum.max(&>=/2, fn -> 0 end)
    new_ct = max_ct + 1

    ct1 = dsu[:jn_to_circuit] |> Map.get(jn1, new_ct)
    ct2 = dsu[:jn_to_circuit] |> Map.get(jn2, new_ct)

    cond do
      ct1 == ct2 and ct1 != new_ct ->
        dsu

      true ->
        circuit_to_jns = dsu[:circuit_to_jns]

        jns1 = Map.get(circuit_to_jns, ct1, MapSet.new())
        jns2 = Map.get(circuit_to_jns, ct2, MapSet.new())

        combined_jns =
          MapSet.union(jns1, jns2)
          |> MapSet.put(jn1)
          |> MapSet.put(jn2)

        min_ct = min(ct1, ct2)

        jn_to_circuit =
          combined_jns
          |> Map.new(fn jn -> {jn, min_ct} end)

        jn_to_circuit = Map.merge(dsu[:jn_to_circuit], jn_to_circuit)

        circuit_to_jns =
          circuit_to_jns
          |> Map.delete(ct1)
          |> Map.delete(ct2)
          |> Map.put(min_ct, combined_jns)

        new(jn_to_circuit, circuit_to_jns)
    end
  end
end

defmodule Solution do
  def parse_line(str) do
    String.split(str, ",") |> Enum.map(&String.to_integer/1) |> List.to_tuple()
  end

  def dist({x1, y1, z1}, {x2, y2, z2}) do
    ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5
  end

  def find_distances_to_all(junctions) do
    junctions
    |> Enum.flat_map(fn jn1 ->
      junctions
      |> Enum.map(fn jn2 ->
        {{jn1, jn2}, dist(jn1, jn2)}
      end)
    end)
    |> Enum.map(fn {{jn1, jn2}, dist} -> {Enum.sort([jn1, jn2]) |> List.to_tuple(), dist} end)
    |> Enum.filter(fn {{jn1, jn2}, _dist} -> jn1 != jn2 end)
    |> Enum.into(%{})
  end

  def solve_part_1(junctions, num_connections) do
    all_dist_map = find_distances_to_all(junctions)

    dist_sorted =
      all_dist_map
      |> Enum.map(fn {{jn1, jn2}, dist} -> {dist, {jn1, jn2}} end)
      |> Enum.sort()

    {dsu, _count} =
      dist_sorted
      |> Enum.reduce_while({DSU.new(), 0}, fn {_dist, {jn1, jn2}}, {dsu, count} ->
        new_dsu = DSU.create_connection(dsu, jn1, jn2)
        new_count = count + 1

        if new_count == num_connections do
          {:halt, {new_dsu, new_count}}
        else
          {:cont, {new_dsu, new_count}}
        end
      end)

    dsu[:circuit_to_jns]
    |> Enum.map(fn {_ct, jns} -> jns |> MapSet.size() end)
    |> Enum.sort(:desc)
    |> Enum.take(3)
    |> Enum.product()
  end

  def solve_part_2(junctions) do
    all_dist_map = find_distances_to_all(junctions)

    dist_sorted =
      all_dist_map
      |> Enum.map(fn {{jn1, jn2}, dist} -> {dist, {jn1, jn2}} end)
      |> Enum.sort()

    num_junctions = length(junctions)

    {_dsu, res} =
      dist_sorted
      |> Enum.reduce_while({DSU.new(), nil}, fn {_dist, {jn1, jn2}}, {dsu, res} ->
        new_dsu = DSU.create_connection(dsu, jn1, jn2)
        cts = new_dsu[:circuit_to_jns] |> Map.keys()

        if length(cts) == 1 and MapSet.size(new_dsu[:circuit_to_jns][cts |> hd]) == num_junctions do
          {{x1, _y1, _z1}, {x2, _y2, _z2}} = {jn1, jn2}
          {:halt, {new_dsu, x1 * x2}}
        else
          {:cont, {new_dsu, res}}
        end
      end)

    res
  end
end

[num_connections_str | junctions_str] =
  "inp8.2.txt"
  |> File.stream!()
  |> Enum.map(&String.trim/1)

num_connections = String.to_integer(num_connections_str)

junctions =
  junctions_str
  |> Enum.map(&Solution.parse_line/1)

IO.puts("Part 1:")

Solution.solve_part_1(junctions, num_connections)
|> IO.inspect()

IO.puts("Part 2:")

Solution.solve_part_2(junctions)
|> IO.inspect()
