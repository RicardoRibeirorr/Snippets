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


// ******************************** OR *************************** //

   public function index(Request $request)
    {
        $users = User::where('is_active', true);

        if ($request->has('age_more_than')) {
            $users->where('age', '>', $request->age_more_than);
        }

        if ($request->has('gender')) {
            $users->where('gender', $request->gender);
        }

        if ($request->has('created_at')) {
            $users->where('created_at','>=', $request->created_at);
        }

        return $users->get();
    }
