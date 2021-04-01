public function filter(Request $request, User $user)
{
    $user = $user->newQuery();

    // Search for a user based on their name.
    if ($request->has('name')) {
        $user->where('name', $request->input('name'));
    }

    // Search for a user based on their company.
    if ($request->has('company')) {
        $user->where('company', $request->input('company'));
    }

    // Search for a user based on their city.
    if ($request->has('city')) {
        $user->where('city', $request->input('city'));
    }

    // Continue for all of the filters.

    // Get the results and return them.
    return $user->get();
}
