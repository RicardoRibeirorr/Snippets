//*************************************************************************************//
// Required Instalation: $ composer require mehdi-fathi/eloquent-filter:1.6.9
//*************************************************************************************//




//*************************************************************************************//
// MODEL
use eloquentFilter\QueryFilter\ModelFilters\Filterable;
class User extends Model
{
    use Filterable;

    private static $whiteListFilter = [
        'id',
        'username',
        'family',
        'email',
        'count_posts',
        'created_at',
        'updated_at',
    ];
// private static $whiteListFilter = ['*']; /* You can set * char for filter in all fields */
}
//*************************************************************************************//



//*************************************************************************************//
// Controller
use eloquentFilter\QueryFilter\ModelFilters\ModelFilters;
class UsersController
{
    public function list(ModelFilters $modelFilters)
    {
          if (!empty($modelFilters->filters())) {
          
              $users = User::filter($modelFilters)->with('posts')->orderByDesc('id')->paginate(10);
          } else {
              $users = User::with('posts')->orderByDesc('id')->paginate(10);
          }
    }
}
//*************************************************************************************//
