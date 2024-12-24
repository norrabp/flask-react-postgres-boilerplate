
interface IUser {
    id: number;
    username: string;
    email: string;
}

const UserCard: React.FC<{user: IUser}> = ({user}) => {
    return (
        <div key={user.id} className="col-md-4 mb-3">
            <div className="card bg-dark">
                <div className="card-body">
                <h5 className="card-title">{user.username}</h5>
                <p className="card-text">{user.email}</p>
                </div>
            </div>
        </div>
    )
}

export default UserCard;