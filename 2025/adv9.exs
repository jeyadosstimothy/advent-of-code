defmodule IOUtil do
  def inspect(item, opts \\ []) do
    # IO.inspect(item, opts)
    item
  end

  def newline() do
    # IO.puts("")
  end
end

defmodule Solution do
  def parse_line(str) do
    String.trim(str)
    |> String.split(",")
    |> Enum.map(&String.to_integer/1)
    |> Enum.reverse()
    |> List.to_tuple()
  end

  def to_segments(coords) do
    coords |> Enum.zip(tl(coords) ++ [hd(coords)])
  end

  def get_bounds({i1, j1}, {i2, j2}) do
    min_i = min(i1, i2)
    max_i = max(i1, i2)
    min_j = min(j1, j2)
    max_j = max(j1, j2)

    {{min_i, max_i}, {min_j, max_j}}
  end

  def calculate_area(c1, c2) do
    {{min_i, max_i}, {min_j, max_j}} = get_bounds(c1, c2)
    (max_i - min_i + 1) * (max_j - min_j + 1)
  end

  def solve_part_1(coords) do
    coords_i = coords |> Enum.with_index()

    areas =
      for {c1, i} <- coords_i, {c2, j} <- coords_i, i < j do
        calculate_area(c1, c2)
      end

    areas |> Enum.max()
  end

  def inside_bounds?({{min_i, max_i}, {min_j, max_j}}, {i, j}) do
    min_i < i and i < max_i and min_j < j and j < max_j
  end

  def dist({i1, j1}, {i2, j2}) do
    abs(i1 - i2) + abs(j1 - j2)
  end

  def get_corners(c1, c2) do
    {{min_i, max_i}, {min_j, max_j}} = get_bounds(c1, c2)

    [{min_i, min_j}, {min_i, max_j}, {max_i, max_j}, {max_i, min_j}]
  end

  def coord_inside?(v_segments, c = {i, j}) do
    IOUtil.inspect(c, label: "c")

    segments_to_the_right =
      v_segments
      |> Enum.filter(fn {{si, sj}, {ei, _ej}} ->
        sj > j and min(si, ei) <= i and i < max(si, ei)
      end)
      |> IOUtil.inspect(label: "segments_to_the_right")

    coord_on_the_segment? =
      v_segments
      |> Enum.filter(fn {{si, sj}, {ei, _ej}} ->
        sj == j and min(si, ei) <= i and i <= max(si, ei)
      end)
      |> Enum.any?()

    odd_segments? = Integer.mod(segments_to_the_right |> length(), 2) != 0
    IOUtil.inspect(coord_on_the_segment?, label: "coord_on_the_segment?")
    IOUtil.inspect(odd_segments?, label: "odd_segments?")
    coord_on_the_segment? or odd_segments?
  end

  def corners_valid?(c1, c2, v_segments) do
    get_corners(c1, c2)
    |> IOUtil.inspect(label: "corners")
    |> Enum.all?(&coord_inside?(v_segments, &1))
    |> IOUtil.inspect(label: "corners_valid?")
  end

  def h_boundaries_valid?({i1, j1}, {i2, j2}, v_segments) do
    IOUtil.inspect({{i1, j1}, {i2, j2}}, label: "{{i1, j1}, {i2, j2}}")

    v_segments_to_the_right =
      v_segments
      |> Enum.filter(fn {{si, sj}, {ei, _ej}} ->
        j1 < sj and sj < j2 and min(si, ei) < i1 and i1 < max(si, ei)
      end)
      |> IOUtil.inspect(label: "v_segments_to_the_right")

    Integer.mod(length(v_segments_to_the_right), 2) == 0 and
      v_segments_to_the_right
      |> Enum.chunk_every(2, 2)
      |> Enum.all?(fn [v_seg1, v_seg2] ->
        {{_si, sj1}, {_ei, _ej}} = v_seg1
        {{_si, sj2}, {_ei, _ej}} = v_seg2
        abs(sj1 - sj2) == 1
      end)
  end

  def v_boundaries_valid?(c1, c2, h_segments) do
    transpose = fn {{si, sj}, {ei, ej}} ->
      [{sj, si}, {ej, ei}] |> Enum.sort() |> List.to_tuple()
    end

    {new_c1, new_c2} = transpose.({c1, c2})

    h_boundaries_valid?(
      new_c1,
      new_c2,
      h_segments |> Enum.map(transpose)
    )
  end

  def boundaries_valid?(c1, c2, v_segments, h_segments) do
    {{min_i, max_i}, {min_j, max_j}} = get_bounds(c1, c2)

    h_boundaries_valid?({min_i, min_j}, {min_i, max_j}, v_segments) and
      h_boundaries_valid?({max_i, min_j}, {max_i, max_j}, v_segments) and
      v_boundaries_valid?({min_i, min_j}, {max_i, min_j}, h_segments) and
      v_boundaries_valid?({min_i, max_j}, {max_i, max_j}, h_segments)
  end

  # Partial implementation to handle cases where corners & boundaries are valid, but there's gap inside the rectangle.
  # Skipping this because input doesnt have this edge case.
  # def v_gap_present_from_c?(c = {i, j}, v_segments) do
  #   (v_segments
  #   |> Enum.filter(fn {{si, sj}, {ei, ej}} -> sj >= j and min(si, ei) <= i and i <= max(si, ei) end)
  #   |> Enum.chunk_every(2, 2)
  #   |> Enum.any?(fn [c1, c2] -> dist(c1, c2) > 1 end))
  #   |> IOUtil.inspect(label: "v_gap_present_from_c?")
  # end

  # def v_gap_present_inside?(c1, c2, coords, v_segments, h_segments) do
  #   {{min_i, max_i}, {min_j, max_j}} = get_bounds(c1, c2)

  #   trimmed_v_segments =
  #     v_segments
  #     |> Enum.filter(fn {{si, sj}, {ei, ej}} ->
  #       min_j <= sj and sj <= max_j and min_i < ei and si < max_i
  #     end)
  #     |> IOUtil.inspect(label: "v_segments_covered")
  #     |> Enum.map(fn {{si, sj}, {ei, ej}} ->
  #       {{max(si, min_i + 1), sj}, {min(ei, max_i - 1), ej}}
  #     end)
  #     |> IOUtil.inspect(label: "trimmed_v_segments")

  #   v_coords_to_check =
  #     trimmed_v_segments
  #     |> Enum.map(fn {{si, _sj}, {_ei, _ej}} -> {si, min_j} end)
  #     |> Enum.sort()
  #     |> Enum.dedup()

  #   v_coords_to_check
  #     |> Enum.filter(&v_gap_present_from_c?(&1, trimmed_v_segments))
  #     |> Enum.any?()
  # end

  # def insides_valid?(c1, c2, coords, v_segments, h_segments) do
  #   true
  # end

  def valid_rectangle?(c1, c2, _coords, v_segments, h_segments) do
    corners_valid?(c1, c2, v_segments) and
      boundaries_valid?(c1, c2, v_segments, h_segments)

    # and insides_valid?(c1, c2, coords, v_segments, h_segments)
  end

  def solve_part_2_geometry(coords) do
    segments = coords |> to_segments()

    v_segments =
      segments
      |> Enum.filter(fn {{_si, sj}, {_ei, ej}} -> sj == ej end)
      |> IOUtil.inspect(label: "v_segments")

    h_segments =
      segments
      |> Enum.filter(fn {{si, _sj}, {ei, _ej}} -> si == ei end)
      |> IOUtil.inspect(label: "h_segments")

    coords_i = coords |> Enum.with_index()

    areas =
      for {c1, i} <- coords_i, {c2, j} <- coords_i, i < j do
        IOUtil.inspect(c1, label: "c1")
        IOUtil.inspect(c2, label: "c2")

        area =
          if valid_rectangle?(c1, c2, coords, v_segments, h_segments) do
            calculate_area(c1, c2)
          else
            0
          end

        IOUtil.inspect(area, label: "area")
        IOUtil.newline()
        area
      end

    areas |> Enum.max()
  end

  def neighbours({i, j}, {{min_i, max_i}, {min_j, max_j}}, boundary_coords, visited) do
    [
      {0, 1},
      {0, -1},
      {-1, 0},
      {1, 0}
    ]
    |> Enum.map(fn {di, dj} -> {i + di, j + dj} end)
    |> Enum.filter(fn {i, j} ->
      min_i < i and i < max_i and min_j < j and j < max_j and {i, j} not in boundary_coords and
        {i, j} not in visited
    end)
  end

  def traverse([], _bounds, _boundary_coords, visited) do
    visited
  end

  def traverse(_queue = [curr | rem], bounds, boundary_coords, visited) do
    next = neighbours(curr, bounds, boundary_coords, visited)

    traverse(rem ++ next, bounds, boundary_coords, MapSet.union(visited, MapSet.new(next)))
  end

  def create_prefix_matrix({{min_i, max_i}, {min_j, max_j}}, outside_points) do
    matrix =
      for i <- min_i..max_i, j <- min_j..max_j, into: %{} do
        {{i, j},
         if {i, j} in outside_points do
           1
         else
           0
         end}
      end

    prefix_matrix =
      matrix
      |> Enum.sort()
      |> Enum.reduce(%{}, fn {{i, j}, x}, acc ->
        Map.put(
          acc,
          {i, j},
          x + Map.get(acc, {i, j - 1}, 0) + Map.get(acc, {i - 1, j}, 0) -
            Map.get(acc, {i - 1, j - 1}, 0)
        )
      end)

    prefix_matrix
  end

  def get_sum_from_prefix_matrix({{si, sj}, {ei, ej}}, prefix_matrix) do
    {{min_i, max_i}, {min_j, max_j}} = get_bounds({si, sj}, {ei, ej})
    IOUtil.inspect({{min_i, max_i}, {min_j, max_j}})

    result =
      Map.get(prefix_matrix, {max_i, max_j}) - Map.get(prefix_matrix, {min_i - 1, max_j}) -
        Map.get(prefix_matrix, {max_i, min_j - 1}) +
        Map.get(prefix_matrix, {min_i - 1, min_j - 1})
  end

  def compress(sequence) do
    sequence_to_idx_dict =
      sequence
      |> Enum.sort()
      |> Enum.dedup()
      |> Enum.with_index()
      |> Enum.map(fn {x, idx} -> {x, idx * 2} end)
      |> Map.new()

    sequence_to_idx_dict_inverse = Map.new(sequence_to_idx_dict, fn {x, idx} -> {idx, x} end)

    idxs = sequence_to_idx_dict_inverse |> Enum.map(&elem(&1, 0))
    bounds = {Enum.min(idxs), Enum.max(idxs)}

    {sequence_to_idx_dict, sequence_to_idx_dict_inverse, bounds}
  end

  def solve_part_2_floodfill(coords) do
    {i_dict, i_dict_inverse, i_bounds} = coords |> Enum.map(&elem(&1, 0)) |> compress()
    {j_dict, j_dict_inverse, j_bounds} = coords |> Enum.map(&elem(&1, 1)) |> compress()
    IOUtil.inspect(i_dict |> Enum.sort(), label: "i_dict", limit: :infinity)
    IOUtil.inspect(j_dict |> Enum.sort(), label: "j_dict", limit: :infinity)

    _actual_bounds = {{min_i, max_i}, {min_j, max_j}} = {i_bounds, j_bounds}

    compressed_coords =
      coords |> Enum.map(fn {i, j} -> {Map.get(i_dict, i), Map.get(j_dict, j)} end)

    boundary_coords =
      to_segments(compressed_coords)
      |> Enum.flat_map(fn {{si, sj}, {ei, ej}} ->
        if si == ei do
          min(sj, ej)..max(sj, ej) |> Enum.map(&{si, &1})
        else
          min(si, ei)..max(si, ei) |> Enum.map(&{&1, sj})
        end
      end)

    bounds_with_buffer = {{min_i - 2, max_i + 2}, {min_j - 2, max_j + 2}}
    start = {min_i - 1, min_j - 1}
    outside_points = traverse([start], bounds_with_buffer, boundary_coords, MapSet.new([start]))
    IOUtil.inspect(outside_points |> Enum.sort(), label: "outside_points")

    prefix_matrix = create_prefix_matrix(bounds_with_buffer, outside_points)
    IOUtil.inspect(prefix_matrix |> Enum.sort(), label: "prefix_matrix", limit: :infinity)

    coords_idx = compressed_coords |> Enum.with_index()

    areas =
      for {c1 = {i1, j1}, idx_i} <- coords_idx,
          {c2 = {i2, j2}, idx_j} <- coords_idx,
          idx_i < idx_j,
          get_sum_from_prefix_matrix({c1, c2}, prefix_matrix) == 0 do
        calculate_area(
          {Map.get(i_dict_inverse, i1), Map.get(j_dict_inverse, j1)},
          {Map.get(i_dict_inverse, i2), Map.get(j_dict_inverse, j2)}
        )
      end

    areas |> Enum.max()
  end
end

coords =
  IO.read(:stdio, :eof)
  |> String.split()
  |> Enum.map(&Solution.parse_line/1)

IO.puts("Part 1:")

Solution.solve_part_1(coords)
|> IO.puts()

IO.puts("Part 2 - Geometry:")

Solution.solve_part_2_geometry(coords)
|> IO.puts()

IO.puts("Part 2 - Floodfill:")

Solution.solve_part_2_floodfill(coords)
|> IO.puts()
